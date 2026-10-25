#!/usr/bin/env python3
"""
Monitor SCL → Cancún: busca precios y avisa por email si hay oferta buena.
Pensado para cron en servidor WFitness (24/7 + internet).
"""

from __future__ import annotations

import json
import os
import re
import smtplib
import ssl
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / "config.env")
load_dotenv(ROOT / ".env")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
}


def env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw.replace(".", "").replace(",", ""))


def state_path() -> Path:
    configured = os.getenv("STATE_PATH")
    if configured:
        return Path(configured)
    return ROOT / "data" / "state.json"


def load_state() -> dict[str, Any]:
    path = state_path()
    if not path.exists():
        return {
            "baseline": {},
            "history": [],
            "last_alert_fingerprint": None,
            "last_check_at": None,
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_clp_amounts(text: str, *, roundtrip_bias: bool = True) -> list[int]:
    """Extrae montos CLP plausibles. Por defecto filtra rango de ida/vuelta."""
    amounts: list[int] = []
    # Ida/vuelta SCL-CUN suele vivir ~380k–1.2M; one-way suele ser más bajo.
    lo, hi = (350_000, 1_800_000) if roundtrip_bias else (150_000, 2_500_000)
    patterns = [
        r"CLP\s*([\d.]+)",
        r"\$\s*([\d.]+)",
        r"([\d]{1,3}(?:\.[\d]{3}){1,2})",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            digits = m.group(1).replace(".", "")
            if not digits.isdigit():
                continue
            val = int(digits)
            if lo <= val <= hi:
                amounts.append(val)
    return amounts


def fetch_text(url: str, timeout: int = 25) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text


def check_despegar() -> dict[str, Any]:
    url = "https://www.despegar.cl/vuelos/scl/cun/vuelos-a-cancun-desde-santiago+de+chile"
    html = fetch_text(url)
    amounts = parse_clp_amounts(BeautifulSoup(html, "html.parser").get_text(" ", strip=True))
    best = min(amounts) if amounts else None
    return {"source": "despegar", "url": url, "best_rt_clp": best, "samples": amounts[:8]}


def check_falabella() -> dict[str, Any]:
    url = (
        "https://www.viajesfalabella.cl/vuelos/scl/cun/"
        "vuelos-a-cancun-desde-santiago+de+chile?di=1-0&from=SB&reSearch=true"
    )
    html = fetch_text(url)
    amounts = parse_clp_amounts(BeautifulSoup(html, "html.parser").get_text(" ", strip=True))
    best = min(amounts) if amounts else None
    return {"source": "falabella", "url": url, "best_rt_clp": best, "samples": amounts[:8]}


def check_kayak() -> dict[str, Any]:
    url = (
        "https://www.kayak.cl/vuelos/"
        "Santiago-de-Chile-Aeropuerto-Internacional-Comodoro-Arturo-Merino-Benitez-SCL/"
        "Cancun-CUN"
    )
    html = fetch_text(url)
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    # Preferir bloque "ida y vuelta" si aparece en el texto
    rt_chunk = text
    for marker in ("ida y vuelta", "Ida y vuelta", "round-trip", "Round-trip"):
        idx = text.lower().find(marker.lower())
        if idx >= 0:
            rt_chunk = text[idx : idx + 800]
            break
    amounts = parse_clp_amounts(rt_chunk, roundtrip_bias=True)
    if not amounts:
        amounts = parse_clp_amounts(text, roundtrip_bias=True)
    best = min(amounts) if amounts else None
    return {"source": "kayak", "url": url, "best_rt_clp": best, "samples": amounts[:8]}


def check_aereos_info() -> dict[str, Any]:
    url = "https://aereos.info/?s=canc%C3%BAn+santiago"
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "aereos.info", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    # USD deals sometimes listed
    usd = re.findall(r"USD\s*([\d.,]+)", text, flags=re.I)
    usd_vals = []
    for u in usd:
        try:
            usd_vals.append(float(u.replace(",", ".")))
        except ValueError:
            pass
    # Filtrar USD plausibles de RT SCL-CUN (~USD 420–900)
    rt_usd = [u for u in usd_vals if 420 <= u <= 1200]
    best_usd = min(rt_usd) if rt_usd else None
    best_clp = int(best_usd * 950) if best_usd else None
    return {
        "source": "aereos.info",
        "url": url,
        "best_rt_clp": best_clp,
        "best_rt_usd": best_usd,
        "samples": rt_usd[:5],
    }


def check_amadeus() -> dict[str, Any] | None:
    client_id = os.getenv("AMADEUS_CLIENT_ID", "").strip()
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        return None

    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_resp = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=20,
    )
    token_resp.raise_for_status()
    token = token_resp.json()["access_token"]

    # Sample March window — adjust as needed
    params = {
        "originLocationCode": "SCL",
        "destinationLocationCode": "CUN",
        "departureDate": "2026-03-12",
        "returnDate": "2026-03-19",
        "adults": 1,
        "children": 1,
        "currencyCode": "CLP",
        "max": 10,
    }
    search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    r = requests.get(
        search_url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    r.raise_for_status()
    offers = r.json().get("data", [])
    prices = []
    for offer in offers:
        try:
            prices.append(int(float(offer["price"]["grandTotal"])))
        except (KeyError, ValueError, TypeError):
            continue
    best = min(prices) if prices else None
    return {
        "source": "amadeus",
        "url": "https://developers.amadeus.com",
        "best_rt_clp": best,
        "samples": prices[:8],
        "note": "total 1 adulto+1 niño para fechas muestra 12–19 mar",
    }


def collect_quotes() -> list[dict[str, Any]]:
    checkers = [check_despegar, check_falabella, check_kayak, check_aereos_info]
    results: list[dict[str, Any]] = []
    for fn in checkers:
        try:
            results.append(fn())
        except Exception as exc:  # noqa: BLE001
            results.append({"source": fn.__name__, "best_rt_clp": None, "error": str(exc)})
    try:
        amadeus = check_amadeus()
        if amadeus:
            results.append(amadeus)
    except Exception as exc:  # noqa: BLE001
        results.append({"source": "amadeus", "best_rt_clp": None, "error": str(exc)})
    return results


def classify(best: int | None) -> str | None:
    if best is None:
        return None
    great = env_int("THRESHOLD_GREAT", 430_000)
    good = env_int("THRESHOLD_GOOD", 500_000)
    if best <= great:
        return "EXCELENTE"
    if best <= good:
        return "BUENA"
    return None


def send_email(subject: str, body: str) -> None:
    to_addr = os.getenv("ALERT_TO", "").strip()
    from_addr = os.getenv("ALERT_FROM", to_addr).strip()
    host = os.getenv("SMTP_HOST", "").strip()
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    use_tls = os.getenv("SMTP_TLS", "true").lower() in {"1", "true", "yes"}

    if not to_addr or not host:
        raise RuntimeError("Falta ALERT_TO o SMTP_HOST en config.env")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    if use_tls:
        context = ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            if user:
                server.login(user, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=30) as server:
            if user:
                server.login(user, password)
            server.send_message(msg)


def search_windows() -> list[dict[str, str]]:
    """Ventanas de fechas a replicar manualmente (prioriza marzo)."""
    raw = os.getenv(
        "SEARCH_WINDOWS",
        "2026-03-07|2026-03-20|prioridad marzo;2026-03-12|2026-03-19|marzo mid;"
        "2026-03-23|2026-03-31|marzo late (ref. USD469);2026-02-28|2026-03-07|puente feb-mar",
    )
    windows: list[dict[str, str]] = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        bits = part.split("|")
        if len(bits) < 2:
            continue
        windows.append(
            {
                "outbound": bits[0].strip(),
                "inbound": bits[1].strip(),
                "label": bits[2].strip() if len(bits) > 2 else "",
            }
        )
    return windows


def format_clp(n: int | None) -> str:
    if n is None:
        return "N/D"
    return f"${n:,}".replace(",", ".")


def format_report(quotes: list[dict[str, Any]], level: str | None, best: int | None) -> str:
    windows = search_windows()
    primary = windows[0] if windows else {
        "outbound": "2026-03-07",
        "inbound": "2026-03-20",
        "label": "prioridad marzo",
    }

    lines = [
        "========================================",
        " ALERTA OFERTAS · Chile → Cancún",
        "========================================",
        f"Check (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
        f"Mejor precio visto: {format_clp(best)} CLP por persona (ida y vuelta)",
        f"Clasificación: {level or 'sin oferta bajo umbral'}",
        "",
        "----------------------------------------",
        " CÓMO REPLICAR LA BÚSQUEDA (copiar tal cual)",
        "----------------------------------------",
        "VUELOS",
        "  Sitio: Google Flights  (recomendado) o Kayak / Despegar",
        "  Origen: Santiago (SCL) — Aeropuerto Arturo Merino Benítez",
        "  Destino: Cancún (CUN)",
        "  Tipo: Ida y vuelta",
        f"  Ida: {primary['outbound']}   Vuelta: {primary['inbound']}"
        + (f"   ({primary['label']})" if primary.get("label") else ""),
        "  Pasajeros: 1 adulto + 1 niño (8 años / categoría 2–11)",
        "  Clase: Económica",
        "  Escalas: da igual (priorizar precio); si puedes, directo LATAM",
        "  Moneda: CLP",
        "",
        "Otras ventanas a probar (mismas personas/clase):",
    ]
    for w in windows[1:]:
        lines.append(
            f"  · Ida {w['outbound']}  /  Vuelta {w['inbound']}"
            + (f"  — {w['label']}" if w.get("label") else "")
        )

    lines += [
        "",
        "HOSPEDAJE (Cancún Norte — playa calmada)",
        "  Zona: Zona Hotelera Km 1–9 (bahía norte)",
        "  Nombres a buscar: Grand Oasis Palm | Occidental Costa Cancún | Riu Caribe",
        "  Fechas hotel: mismas que el vuelo (noche de llegada = día de ida)",
        "  Huéspedes: 1 adulto + 1 niño",
        "  Preferencia: Todo incluido si el precio es razonable",
        "  Evitar para nadar con niña: Km 9–20 / Playa Delfines (más oleaje)",
        "",
        "PASOS RÁPIDOS EN GOOGLE FLIGHTS",
        "  1) Entrá a google.com/travel/flights (Chile / CLP)",
        "  2) Completá los parámetros de VUELOS de arriba",
        "  3) Ordená por precio y anotá el más barato",
        "  4) Si está bajo umbral EXCELENTE, conviene comprar",
        "",
        "----------------------------------------",
        " PRECIOS DETECTADOS EN ESTE CHECK",
        "----------------------------------------",
    ]
    for q in quotes:
        err = q.get("error")
        src = q.get("source")
        if err:
            lines.append(f"- {src}: sin dato ({err[:80]})")
        else:
            extra = f" | USD {q['best_rt_usd']}" if q.get("best_rt_usd") else ""
            lines.append(f"- {src}: {format_clp(q.get('best_rt_clp'))} CLP{extra}")

    lines += [
        "",
        "Umbrales (por persona, ida/vuelta):",
        f"  BUENA ≤ {format_clp(env_int('THRESHOLD_GOOD', 500_000))}",
        f"  EXCELENTE ≤ {format_clp(env_int('THRESHOLD_GREAT', 430_000))}",
        f"  Paquete vuelo+hotel ≤ {format_clp(env_int('THRESHOLD_PACKAGE', 950_000))}",
        "",
        "Nota: no dependas de links automáticos (a veces abren la home).",
        "Usá siempre estos parámetros para simular la misma búsqueda.",
        "Monitor WFitness · cada pocas horas · aristides20@gmail.com",
    ]
    return "\n".join(lines)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    force_mail = "--force-mail" in sys.argv

    quotes = collect_quotes()
    priced = [q["best_rt_clp"] for q in quotes if isinstance(q.get("best_rt_clp"), int)]
    best = min(priced) if priced else None
    level = classify(best)

    state = load_state()
    now = datetime.now(timezone.utc).isoformat()
    entry = {"at": now, "best_rt_clp": best, "level": level, "quotes": quotes}
    history = state.get("history", [])
    history.append(entry)
    state["history"] = history[-60:]  # keep last 60 checks
    state["last_check_at"] = now
    if not state.get("baseline"):
        state["baseline"] = {"best_rt_clp": best, "captured_at": now}

    fingerprint = f"{level}:{best}"
    should_alert = bool(level) and (
        force_mail or state.get("last_alert_fingerprint") != fingerprint
    )

    report = format_report(quotes, level, best)
    print(report)

    if should_alert and not dry_run:
        subject = f"[Cancún] Oferta {level}: ~${best:,} CLP/pp SCL-CUN".replace(",", ".")
        send_email(subject, report)
        state["last_alert_fingerprint"] = fingerprint
        print(f"\nEmail enviado a {os.getenv('ALERT_TO')}")
    elif dry_run:
        print("\n(dry-run: no se envió email)")
    else:
        print("\nSin alerta (sin umbral nuevo o mismo fingerprint).")

    save_state(state)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        raise SystemExit(1)

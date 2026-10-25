#!/usr/bin/env python3
"""
Monitor SCL → Valencia, Venezuela (VLN).
Ida ~20–23 dic / vuelta ~30 dic. Avisos por email con parámetros copy-paste.
Compra recomendada: web de la aerolínea (Copa / Avianca).
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
    configured = os.getenv("VLN_STATE_PATH")
    if configured:
        return Path(configured)
    return ROOT / "data" / "state_vln.json"


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


def parse_clp_amounts(text: str, *, lo: int = 550_000, hi: int = 2_000_000) -> list[int]:
    amounts: list[int] = []
    patterns = [
        r"CLP\s*([\d.,]+)",
        r"\$\s*([\d.]+)",
        r"([\d]{1,3}(?:\.[\d]{3}){1,2})",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            digits = m.group(1).replace(".", "").replace(",", "")
            if not digits.isdigit():
                continue
            val = int(digits)
            if lo <= val <= hi:
                amounts.append(val)
    return amounts


def parse_usd_to_clp(text: str, *, lo: float = 550, hi: float = 1500) -> tuple[int | None, float | None]:
    usd = re.findall(r"USD\s*([\d.,]+)", text, flags=re.I)
    vals: list[float] = []
    for u in usd:
        try:
            vals.append(float(u.replace(",", "")))
        except ValueError:
            continue
    rt = [v for v in vals if lo <= v <= hi]
    if not rt:
        return None, None
    best = min(rt)
    return int(best * 950), best


def fetch_text(url: str, timeout: int = 25) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text


def check_kayak_vln() -> dict[str, Any]:
    url = (
        "https://www.kayak.cl/flights?"
        "origin=SCL&destination=VLN&depart_date=2026-12-22&return_date=2026-12-30"
        "&adults=1&cabin=e&oneway=n&sort=price_a"
    )
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "kayak", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    amounts = parse_clp_amounts(text)
    best = min(amounts) if amounts else None
    return {"source": "kayak", "url": url, "best_rt_clp": best, "samples": amounts[:8]}


def check_momondo_vln() -> dict[str, Any]:
    url = "https://www.es.momondo.com/vuelos/santiago-de-chile/valencia-estado-carabobo"
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "momondo", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    # momondo often shows USD
    clp_from_usd, usd = parse_usd_to_clp(text)
    amounts = parse_clp_amounts(text)
    best = min(amounts) if amounts else clp_from_usd
    return {
        "source": "momondo",
        "url": url,
        "best_rt_clp": best,
        "best_rt_usd": usd,
        "samples": amounts[:8],
    }


def check_copa_vln() -> dict[str, Any]:
    url = "https://www.copaair.com/es-cl/vuelos-desde-santiago-de-chile-a-valencia-(venezuela)"
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "copa", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    amounts = parse_clp_amounts(text, lo=500_000, hi=1_500_000)
    clp_usd, usd = parse_usd_to_clp(text, lo=600, hi=1200)
    # Prefer December mention near prices if possible
    best = min(amounts) if amounts else clp_usd
    return {
        "source": "copa",
        "url": url,
        "best_rt_clp": best,
        "best_rt_usd": usd,
        "samples": amounts[:8],
        "note": "tarifas mensuales en landing Copa (dic suele ~USD 780–830)",
    }


def check_edreams_vln() -> dict[str, Any]:
    url = "https://cl.edreams.com/vuelos/santiago-de-chile-valencia/SCL/VLN/"
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "edreams", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    amounts = parse_clp_amounts(text)
    best = min(amounts) if amounts else None
    return {"source": "edreams", "url": url, "best_rt_clp": best, "samples": amounts[:8]}


def collect_quotes() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for fn in (check_copa_vln, check_kayak_vln, check_momondo_vln, check_edreams_vln):
        try:
            results.append(fn())
        except Exception as exc:  # noqa: BLE001
            results.append({"source": fn.__name__, "best_rt_clp": None, "error": str(exc)})
    return results


def classify(best: int | None) -> str | None:
    if best is None:
        return None
    # Dic Navidad: umbrales más altos que Cancún marzo
    great = env_int("VLN_THRESHOLD_GREAT", 700_000)
    good = env_int("VLN_THRESHOLD_GOOD", 800_000)
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


def format_clp(n: int | None) -> str:
    if n is None:
        return "N/D"
    return f"${n:,}".replace(",", ".")


def search_windows() -> list[dict[str, str]]:
    raw = os.getenv(
        "VLN_SEARCH_WINDOWS",
        "2026-12-20|2026-12-30|opción A;2026-12-21|2026-12-30|opción B;"
        "2026-12-22|2026-12-30|opción C;2026-12-23|2026-12-30|opción D;"
        "2026-12-22|2026-12-31|flexible vuelta",
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


def format_report(quotes: list[dict[str, Any]], level: str | None, best: int | None) -> str:
    windows = search_windows()
    primary = windows[0] if windows else {
        "outbound": "2026-12-22",
        "inbound": "2026-12-30",
        "label": "",
    }
    lines = [
        "========================================",
        " ALERTA · Chile → Valencia (Venezuela)",
        "========================================",
        f"Check (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
        f"Mejor precio visto: {format_clp(best)} CLP/pp ida y vuelta",
        f"Clasificación: {level or 'sin oferta bajo umbral'}",
        "",
        "----------------------------------------",
        " PARÁMETROS PARA REPLICAR (copiar tal cual)",
        "----------------------------------------",
        "VUELOS",
        "  Origen: Santiago (SCL)",
        "  Destino: Valencia VE — Arturo Michelena (VLN)",
        "           (NO Valencia España / VLC)",
        "  Tipo: Ida y vuelta · Económica · CLP",
        f"  Ida: {primary['outbound']}   Vuelta: {primary['inbound']}"
        + (f"   ({primary['label']})" if primary.get("label") else ""),
        "  Pasajeros: 1 adulto (sumá niño 2–11 si aplica)",
        "  Sin directo: 1 escala (Copa vía Panamá o Avianca vía Bogotá)",
        "",
        "Otras ventanas:",
    ]
    for w in windows[1:]:
        lines.append(
            f"  · Ida {w['outbound']} / Vuelta {w['inbound']}"
            + (f" — {w['label']}" if w.get("label") else "")
        )

    lines += [
        "",
        "COMPRA",
        "  1) Google Flights / Kayak solo para ver precio y aerolínea",
        "  2) Comprar DIRECTO en: copaair.com  o  avianca.com",
        "  3) NUNCA SmartFares / Kayak Mix",
        "",
        "ALTERNATIVA",
        "  Si VLN sale caro: SCL → Caracas (CCS) + traslado terrestre ~2.5–4 h a Valencia",
        "",
        "----------------------------------------",
        " PRECIOS DE ESTE CHECK",
        "----------------------------------------",
    ]
    for q in quotes:
        if q.get("error"):
            lines.append(f"- {q.get('source')}: sin dato ({str(q['error'])[:80]})")
        else:
            extra = f" | USD {q['best_rt_usd']}" if q.get("best_rt_usd") else ""
            lines.append(f"- {q.get('source')}: {format_clp(q.get('best_rt_clp'))} CLP{extra}")

    lines += [
        "",
        "Umbrales VLN (dic/Navidad, por persona RT):",
        f"  BUENA ≤ {format_clp(env_int('VLN_THRESHOLD_GOOD', 800_000))}",
        f"  EXCELENTE ≤ {format_clp(env_int('VLN_THRESHOLD_GREAT', 700_000))}",
        "",
        "Monitor WFitness · aristides20@gmail.com",
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
    history = state.get("history", [])
    history.append({"at": now, "best_rt_clp": best, "level": level, "quotes": quotes})
    state["history"] = history[-60:]
    state["last_check_at"] = now
    if not state.get("baseline"):
        state["baseline"] = {"best_rt_clp": best, "captured_at": now}

    fingerprint = f"VLN:{level}:{best}"
    should_alert = bool(level) and (
        force_mail or state.get("last_alert_fingerprint") != fingerprint
    )

    report = format_report(quotes, level, best)
    print(report)

    if should_alert and not dry_run:
        subject = f"[VLN] Oferta {level}: ~{format_clp(best)} CLP/pp SCL-Valencia VE"
        send_email(subject, report)
        state["last_alert_fingerprint"] = fingerprint
        print(f"\nEmail enviado a {os.getenv('ALERT_TO')}")
    elif dry_run:
        print("\n(dry-run: no se envió email)")
    else:
        print("\nSin alerta VLN (sin umbral nuevo o mismo fingerprint).")

    save_state(state)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        raise SystemExit(1)

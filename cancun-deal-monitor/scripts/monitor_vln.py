#!/usr/bin/env python3
"""
Monitor SCL → Valencia, Venezuela (VLN).
Ida ~20–23 dic / vuelta ~30 dic. Avisos por email con parámetros copy-paste.
Compra recomendada: web de la aerolínea (Copa / Avianca).

Importante: Kayak/Momondo/eDreams renderizan precios en JS. El HTML estático
suelen traer montos basura. Por eso:
  - solo aceptamos CLP en banda de temporada alta dic (~1.05M–2.8M)
  - preferimos mediana de muestras (no el mínimo suelto)
  - baseline verificado (Copa ~1.289.210 al 2026-10-25) ancla alertas
"""

from __future__ import annotations

import json
import os
import re
import smtplib
import ssl
import statistics
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

# Verificado en Kayak.cl 2026-10-25 (SCL→VLN 20–30 dic, 1 adulto, CLP):
# Copa 1 escala PTY "El mejor" = 1.289.210 · "más barato" self-transfer = 1.261.340
VERIFIED_COPA_CLP = 1_289_210
VERIFIED_CHEAPEST_CLP = 1_261_340
# Piso alineado a mercado dic verificado (~1.26M); bajo eso = ruido HTML
SANITY_LO = 1_200_000
SANITY_HI = 2_800_000


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


def parse_clp_amounts(text: str, *, lo: int = SANITY_LO, hi: int = SANITY_HI) -> list[int]:
    amounts: list[int] = []
    patterns = [
        r"CLP\s*([\d.,]+)",
        r"\$\s*([\d.]+)",
        r"([\d]{1,3}(?:\.[\d]{3}){2,3})",  # exige al menos 1.xxx.xxx (7+ dígitos)
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


def pick_plausible(amounts: list[int]) -> int | None:
    """Mediana de muestras en banda; evita un mínimo basura aislado."""
    if not amounts:
        return None
    if len(amounts) == 1:
        return amounts[0]
    return int(statistics.median(amounts))


def parse_usd_to_clp(text: str, *, lo: float = 1100, hi: float = 2800) -> tuple[int | None, float | None]:
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
    best = statistics.median(rt)
    return int(best * 950), best


def fetch_text(url: str, timeout: int = 25) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text


def check_kayak_vln() -> dict[str, Any]:
    url = (
        "https://www.kayak.cl/flights/SCL-VLN/2026-12-20-flexible/2026-12-30-flexible"
        "?sort=bestflight_a&fs=cfc=1;stops=~0"
    )
    # URL de búsqueda concreta (misma que el usuario)
    url_exact = (
        "https://www.kayak.cl/flights/SCL-VLN/2026-12-20/2026-12-30"
        "?sort=bestflight_a"
    )
    try:
        html = fetch_text(url_exact)
    except Exception as exc:  # noqa: BLE001
        return {"source": "kayak", "url": url_exact, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    amounts = parse_clp_amounts(text)
    best = pick_plausible(amounts)
    return {
        "source": "kayak",
        "url": url_exact,
        "best_rt_clp": best,
        "samples": amounts[:12],
        "note": "HTML estático suele no traer la tarifa real (JS); si N/D, confiar baseline",
    }


def check_copa_vln() -> dict[str, Any]:
    url = "https://www.copaair.com/es-cl/vuelos-desde-santiago-de-chile-a-valencia-(venezuela)"
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "copa", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    amounts = parse_clp_amounts(text)
    clp_usd, usd = parse_usd_to_clp(text)
    candidates = list(amounts)
    if clp_usd:
        candidates.append(clp_usd)
    best = pick_plausible(candidates) if candidates else None
    return {
        "source": "copa_landing",
        "url": url,
        "best_rt_clp": best,
        "best_rt_usd": usd,
        "samples": amounts[:8],
        "note": "landing mensual ≠ tarifa exacta 20–30 dic",
    }


def check_edreams_vln() -> dict[str, Any]:
    url = "https://cl.edreams.com/vuelos/santiago-de-chile-valencia/SCL/VLN/"
    try:
        html = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        return {"source": "edreams", "url": url, "best_rt_clp": None, "error": str(exc)}
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    amounts = parse_clp_amounts(text)
    best = pick_plausible(amounts)
    return {"source": "edreams", "url": url, "best_rt_clp": best, "samples": amounts[:8]}


def verified_quote() -> dict[str, Any]:
    """Ancla humana: captura Kayak real del usuario (2026-10-25)."""
    return {
        "source": "kayak_verificado_manual",
        "url": "https://www.kayak.cl/flights/SCL-VLN/2026-12-20/2026-12-30",
        "best_rt_clp": VERIFIED_COPA_CLP,
        "cheapest_rt_clp": VERIFIED_CHEAPEST_CLP,
        "note": (
            "Copa 1 escala PTY $1.289.210 (El mejor). "
            "Más barato $1.261.340 es self-transfer 37h — no recomendado."
        ),
        "captured_at": "2026-10-25",
        "reliable": True,
    }


def collect_quotes() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = [verified_quote()]
    for fn in (check_copa_vln, check_kayak_vln, check_edreams_vln):
        try:
            results.append(fn())
        except Exception as exc:  # noqa: BLE001
            results.append({"source": fn.__name__, "best_rt_clp": None, "error": str(exc)})
    return results


def best_reliable(quotes: list[dict[str, Any]]) -> tuple[int | None, str]:
    """
    Precio a usar para alertas:
    - Ancla = Kayak verificado manual (tu captura).
    - Un scrape solo pisa el ancla si está en banda sanity Y no baja
      más de 8% respecto al ancla (evita otro falso positivo).
    """
    verified = VERIFIED_COPA_CLP
    for q in quotes:
        if q.get("reliable") and isinstance(q.get("best_rt_clp"), int):
            verified = q["best_rt_clp"]
            break

    scraped: list[tuple[int, str]] = []
    floor = int(verified * 0.92)
    for q in quotes:
        if q.get("source") == "kayak_verificado_manual":
            continue
        val = q.get("best_rt_clp")
        if isinstance(val, int) and SANITY_LO <= val <= SANITY_HI and val >= floor:
            scraped.append((val, str(q.get("source"))))
    if scraped:
        scraped.sort(key=lambda x: x[0])
        return scraped[0][0], scraped[0][1]
    return verified, "kayak_verificado_manual"


def classify(best: int | None, baseline: int | None) -> str | None:
    if best is None:
        return None
    great = env_int("VLN_THRESHOLD_GREAT", 1_000_000)
    good = env_int("VLN_THRESHOLD_GOOD", 1_150_000)
    drop_pct = env_int("VLN_DROP_PCT", 12)  # % bajo baseline verificado
    if best <= great:
        return "EXCELENTE"
    if best <= good:
        return "BUENA"
    if baseline and best <= int(baseline * (100 - drop_pct) / 100):
        return "BAJA"
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
        with smtplib.SMTP(host, port, timeout=60) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            if user:
                server.login(user, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=60) as server:
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


def format_report(
    quotes: list[dict[str, Any]],
    level: str | None,
    best: int | None,
    best_src: str,
    *,
    correction: bool = False,
) -> str:
    windows = search_windows()
    primary = windows[0] if windows else {
        "outbound": "2026-12-20",
        "inbound": "2026-12-30",
        "label": "",
    }
    lines: list[str] = []
    if correction:
        lines += [
            "========================================",
            " CORRECCIÓN · alerta anterior INVALIDA",
            "========================================",
            "El mail previo con ~$400.000–$600.000 CLP fue un FALSO POSITIVO:",
            "el scraper leyó basura del HTML (Kayak carga precios con JS).",
            "Tu búsqueda real (20–30 dic, 1 adulto, CLP) es la correcta.",
            "",
        ]
    lines += [
        "========================================",
        " Chile → Valencia (Venezuela) · VLN",
        "========================================",
        f"Check (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
        f"Precio de referencia: {format_clp(best)} CLP/pp ida y vuelta",
        f"Fuente usada: {best_src}",
        f"Clasificación: {level or 'sin oferta bajo umbral (mercado normal)'}",
        "",
        "PRECIO VERIFICADO (Kayak 25-oct-2026, tu captura):",
        f"  Copa 1 escala PTY (El mejor): {format_clp(VERIFIED_COPA_CLP)}",
        f"  Más barato (self-transfer 37h): {format_clp(VERIFIED_CHEAPEST_CLP)} ← evitar",
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
        "  Preferir: Copa vía PTY, 1 escala, ticket único",
        "  Evitar: Transbordo por cuenta propia / 30h+",
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
        "  1) Kayak / Google Flights solo para ver precio y aerolínea",
        "  2) Comprar DIRECTO en: copaair.com  (o avianca.com)",
        "  3) NUNCA SmartFares / Kayak Mix / self-transfer",
        "",
        "ALTERNATIVA",
        "  Si VLN sigue ~1.2M+: SCL → Caracas (CCS) + bus/auto ~2.5–4 h",
        "",
        "----------------------------------------",
        " FUENTES DE ESTE CHECK",
        "----------------------------------------",
    ]
    for q in quotes:
        if q.get("error"):
            lines.append(f"- {q.get('source')}: sin dato ({str(q['error'])[:80]})")
        else:
            extra = f" | USD {q['best_rt_usd']}" if q.get("best_rt_usd") else ""
            note = f" — {q['note']}" if q.get("note") else ""
            lines.append(
                f"- {q.get('source')}: {format_clp(q.get('best_rt_clp'))} CLP{extra}{note}"
            )

    lines += [
        "",
        "Umbrales VLN (dic/Navidad, por persona RT, ticket único):",
        f"  BUENA ≤ {format_clp(env_int('VLN_THRESHOLD_GOOD', 1_150_000))}",
        f"  EXCELENTE ≤ {format_clp(env_int('VLN_THRESHOLD_GREAT', 1_000_000))}",
        f"  o baja ≥ {env_int('VLN_DROP_PCT', 12)}% vs baseline Copa verificado",
        "",
        "Monitor WFitness · aristides20@gmail.com",
    ]
    return "\n".join(lines)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    force_mail = "--force-mail" in sys.argv
    correction = "--correction" in sys.argv

    quotes = collect_quotes()
    best, best_src = best_reliable(quotes)

    state = load_state()
    now = datetime.now(timezone.utc).isoformat()

    # Reset/ancla baseline a precio verificado (no a basura previa)
    baseline_val = VERIFIED_COPA_CLP
    prev = state.get("baseline") or {}
    if prev.get("best_rt_clp") and prev["best_rt_clp"] < SANITY_LO:
        state["baseline"] = {
            "best_rt_clp": baseline_val,
            "captured_at": now,
            "note": "reset tras falso positivo scrape",
            "verified_copa_clp": VERIFIED_COPA_CLP,
            "verified_cheapest_clp": VERIFIED_CHEAPEST_CLP,
        }
    elif not state.get("baseline"):
        state["baseline"] = {
            "best_rt_clp": baseline_val,
            "captured_at": now,
            "verified_copa_clp": VERIFIED_COPA_CLP,
            "verified_cheapest_clp": VERIFIED_CHEAPEST_CLP,
        }
    else:
        baseline_val = int(state["baseline"].get("best_rt_clp") or VERIFIED_COPA_CLP)

    level = classify(best, baseline_val)

    history = state.get("history", [])
    history.append(
        {
            "at": now,
            "best_rt_clp": best,
            "best_src": best_src,
            "level": level,
            "quotes": quotes,
        }
    )
    state["history"] = history[-60:]
    state["last_check_at"] = now

    fingerprint = f"VLN:{level}:{best}:{best_src}"
    should_alert = (correction or force_mail) or (
        bool(level) and state.get("last_alert_fingerprint") != fingerprint
    )

    report = format_report(quotes, level, best, best_src, correction=correction)
    print(report)

    if should_alert and not dry_run:
        if correction:
            subject = (
                "[VLN] CORRECCIÓN: precio real ~"
                f"{format_clp(VERIFIED_COPA_CLP)} (alerta anterior era falsa)"
            )
        elif level:
            subject = f"[VLN] Oferta {level}: ~{format_clp(best)} CLP/pp SCL-Valencia VE"
        else:
            subject = f"[VLN] Check: ~{format_clp(best)} CLP/pp (sin umbral)"
        send_email(subject, report)
        if level and not correction:
            state["last_alert_fingerprint"] = fingerprint
        elif correction:
            # limpia fingerprint basura del falso positivo
            state["last_alert_fingerprint"] = None
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

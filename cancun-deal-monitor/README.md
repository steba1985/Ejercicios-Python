# Monitor ofertas vuelos (Cancún + Valencia VE)

Scripts para el servidor **WFitness** (24/7 + internet): revisan precios y avisan por **correo** cuando hay oferta buena.

## Qué hace

### Cancún (`scripts/monitor.py`)
- Consulta Despegar, Viajes Falabella, Kayak y aereos.info (opcional Amadeus).
- Umbrales por defecto: buena ≤ $500.000 / excelente ≤ $430.000 CLP/pp.
- Estado en `data/state.json`. Cron cada 3h; Black Friday (24–30 nov) más frecuente.

### Valencia VE (`scripts/monitor_vln.py`)
- Destino **VLN** (Arturo Michelena) — no confundir con VLC España.
- Ventanas dic 2026: ida ~20–23 / vuelta ~30.
- Umbrales: BUENA ≤ $800.000 / EXCELENTE ≤ $700.000 CLP/pp (alta temporada).
- Compra recomendada: Copa / Avianca directo. Estado en `data/state_vln.json`.

## Requisitos en el servidor

- Python 3.10+
- Acceso saliente HTTPS
- SMTP que ya use WFitness para mails (o Gmail App Password)

## Instalación rápida

```bash
# En el servidor WFitness
cd /tmp
git clone <este-repo> cancun-tmp   # o scp -r cancun-deal-monitor/
cd cancun-tmp/cancun-deal-monitor
sudo bash scripts/install-cron.sh /var/www/cancun-deal-monitor
sudo nano /var/www/cancun-deal-monitor/config.env   # SMTP + ALERT_TO
```

Prueba:

```bash
/var/www/cancun-deal-monitor/.venv/bin/python \
  /var/www/cancun-deal-monitor/scripts/monitor.py --dry-run

# Enviar un mail de prueba (aunque no haya oferta)
.../monitor.py --force-mail
.../monitor_vln.py --force-mail
```

## config.env (mínimo)

```env
ALERT_TO=aristides20@gmail.com
ALERT_FROM=noreply@wfitness.cl
SMTP_HOST=...          # el del CRM
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_TLS=true
STATE_PATH=/home/ubuntu/cancun-deal-monitor/data/state.json
VLN_THRESHOLD_GOOD=800000
VLN_THRESHOLD_GREAT=700000
VLN_STATE_PATH=/home/ubuntu/cancun-deal-monitor/data/state_vln.json
```

## Notas

- Este monitor es **personal** (vacaciones). No toca módulos del CRM (clases, nómina, EVO).
- Sitios de viajes cambian HTML; si una fuente falla, las otras siguen. Amadeus (opcional) da precios más estables.
- Black Friday: conviene sobre todo para **hotel/paquete**; un vuelo marzo ya barato no hay que “esperar BF”.
- VLN en diciembre es temporada alta; umbrales más altos que Cancún marzo.

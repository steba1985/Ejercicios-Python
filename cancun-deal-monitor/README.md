# Monitor ofertas Cancún (SCL → CUN)

Script para el servidor **WFitness** (24/7 + internet): revisa precios de vuelos y te avisa por **correo** cuando hay oferta buena.

## Qué hace

- Consulta Despegar, Viajes Falabella, Kayak y aereos.info (opcional Amadeus).
- Compara contra umbrales (por defecto: buena ≤ $500.000 / excelente ≤ $430.000 CLP por persona).
- Envía email solo cuando aparece un umbral nuevo (no spamea).
- Guarda historial en `data/state.json`.
- Cron: cada 6 horas; en Black Friday (24–30 nov) cada 4 horas.

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
STATE_PATH=/var/www/cancun-deal-monitor/data/state.json
```

## Notas

- Este monitor es **personal** (vacaciones). No toca módulos del CRM (clases, nómina, EVO).
- Sitios de viajes cambian HTML; si una fuente falla, las otras siguen. Amadeus (opcional) da precios más estables.
- Black Friday: conviene sobre todo para **hotel/paquete**; un vuelo marzo ya barato no hay que “esperar BF”.

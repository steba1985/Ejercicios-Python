#!/usr/bin/env bash
# Instala el monitor en el servidor (Ubuntu/Debian o similar).
# Uso (como root o con sudo):
#   sudo bash scripts/install-cron.sh /var/www/cancun-deal-monitor

set -euo pipefail

TARGET="${1:-/var/www/cancun-deal-monitor}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "→ Instalando en $TARGET"
mkdir -p "$TARGET/data" "$TARGET/scripts" "$TARGET/logs"
rsync -a --exclude 'config.env' --exclude '.env' --exclude 'data/' --exclude '__pycache__' \
  "$SRC/" "$TARGET/"

if [[ ! -f "$TARGET/config.env" ]]; then
  cp "$TARGET/config.example.env" "$TARGET/config.env"
  echo "⚠ Edita $TARGET/config.env con SMTP y umbrales antes de confiar en el cron."
fi

python3 -m venv "$TARGET/.venv"
"$TARGET/.venv/bin/pip" install --upgrade pip
"$TARGET/.venv/bin/pip" install -r "$TARGET/requirements.txt"

CRON_LINE="0 */6 * * * cd $TARGET && $TARGET/.venv/bin/python $TARGET/scripts/monitor.py >> $TARGET/logs/monitor.log 2>&1"
# Black Friday / Cyber Week: cada 4h del 24 al 30 de noviembre
BF_LINE="0 */4 24-30 11 * cd $TARGET && $TARGET/.venv/bin/python $TARGET/scripts/monitor.py >> $TARGET/logs/monitor.log 2>&1"

TMP="$(mktemp)"
crontab -l 2>/dev/null | grep -v 'cancun-deal-monitor' >"$TMP" || true
echo "$CRON_LINE" >>"$TMP"
echo "$BF_LINE" >>"$TMP"
crontab "$TMP"
rm -f "$TMP"

echo "→ Cron instalado (cada 6h + BF nov 24–30 cada 4h)"
echo "→ Prueba manual:"
echo "   $TARGET/.venv/bin/python $TARGET/scripts/monitor.py --dry-run"
echo "   $TARGET/.venv/bin/python $TARGET/scripts/monitor.py --force-mail"

#!/bin/bash
# Run on the droplet as root after: cd /home/wedding/app && git pull
set -euo pipefail

APP_DIR="${APP_DIR:-/home/wedding/app}"
ENV_FILE="/etc/wedding/env"
SERVICE_FILE="/etc/systemd/system/wedding.service"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/setup-production.sh"
  exit 1
fi

if [[ ! -d "$APP_DIR/.venv" ]]; then
  echo "Missing venv at $APP_DIR/.venv"
  exit 1
fi

SECRET_KEY="$("$APP_DIR/.venv/bin/python" -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")"

mkdir -p /etc/wedding
if [[ -f "$ENV_FILE" ]]; then
  cp "$ENV_FILE" "${ENV_FILE}.bak.$(date +%Y%m%d%H%M%S)"
  echo "Backed up existing $ENV_FILE"
fi

cat >"$ENV_FILE" <<EOF
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=${SECRET_KEY}
DJANGO_ALLOWED_HOSTS=nikita-anastasia.com,www.nikita-anastasia.com,167.71.2.126
DJANGO_CSRF_TRUSTED_ORIGINS=https://nikita-anastasia.com,https://www.nikita-anastasia.com
EOF
chmod 600 "$ENV_FILE"
chown root:root "$ENV_FILE"
echo "Wrote $ENV_FILE"

install -m 644 "$APP_DIR/deploy/wedding.service" "$SERVICE_FILE"
systemctl daemon-reload
systemctl enable wedding.service
systemctl restart wedding.service

echo ""
echo "Checking service..."
sleep 1
systemctl is-active wedding.service

echo ""
echo "Django settings check:"
sudo -u wedding bash -lc "cd $APP_DIR && source .venv/bin/activate && python -c \"
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.conf import settings
print('DEBUG:', settings.DEBUG)
print('SECRET_KEY ok:', not settings.SECRET_KEY.startswith('django-insecure'))
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
\""

echo ""
echo "Done. Optional: sudo ufw allow OpenSSH && sudo ufw allow 'Nginx Full' && sudo ufw enable"

#!/bin/bash
PORT=${1:-51852}

SCRIPT_PATH=$(readlink -f "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
APP_DIR=$(dirname "$SCRIPT_DIR")

CURRENT_USER=$(whoami)

sudo tee /etc/systemd/system/dashboard.service > /dev/null <<EOF
[Unit]
Description=Dashboard Rettrice
After=network.target ollama.service
Requires=ollama.service

[Service]
User=${CURRENT_USER}
# 1. NO VIRGOLETTE per WorkingDirectory: systemd legge tutto fino a fine riga
WorkingDirectory=${APP_DIR}
Environment="PORT=${PORT}"
# 2. SI VIRGOLETTE per l'eseguibile di ExecStart (perché ha parametri successivi)
ExecStart="${APP_DIR}/.venv/bin/gunicorn" -w 2 -b 0.0.0.0:${PORT} --log-level info app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl restart dashboard
#!/bin/bash

PORT=${1:-51852}  # usa $1 se fornito, altrimenti 51852 come default

sudo tee /etc/systemd/system/dashboard.service > /dev/null <<EOF
[Unit]
Description=Dashboard Rettrice
After=network.target ollama.service
Requires=ollama.service

[Service]
User=webserver
WorkingDirectory=/home/webserver/dashboard-rettrice
Environment="PORT=${PORT}"
ExecStart=/home/webserver/dashboard-rettrice/.venv/bin/gunicorn -w 2 -b 0.0.0.0:${PORT} --log-level info app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl restart dashboard
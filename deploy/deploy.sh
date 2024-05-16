#!/bin/bash

apt install python3.11-venv

echo "Creating venv..."
python3 -m venv .venv
echo "Activating venv..."
source .venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Installing gunicorn..."
pip install gunicorn

echo "Telling Flask it is behind a proxy..."
touch proxy

echo "Creating service config..."
cat > /etc/systemd/system/uon-ce.service <<EOF
[Unit]
Description=UON CE Gunicorn Daemon
After=network.target

[Service]
User=${USER}
Group=${USER}
WorkingDirectory=${PWD}/src
Environment="PATH=${PWD}/.venv/bin"
ExecStart=${PWD}/.venv/bin/gunicorn --bind 127.0.0.1:5100 app:get_app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

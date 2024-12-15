#!/bin/bash

database_file="$HOME/ce.sqlite3"
bind_address="127.0.0.1:5100"

main() {
  echo "Downloading database..."
  curl "$1" --progress-bar --output "$database_file" || return 1

  echo "Creating venv..."
  python -m venv .venv || return 1

  echo "Activating venv..."
  source .venv/bin/activate || return 1

  echo "Installing requirements..."
  pip install -r requirements.txt || return 1

  echo "Installing gunicorn..."
  pip install gunicorn || return 1

  echo "Creating service config..."
  cat > /etc/systemd/system/uon-ce.service <<EOF || return 1
[Unit]
Description=UON CE Gunicorn Daemon
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$PWD/src
Environment="PATH=$PWD/.venv/bin"
Environment="CE_PROXY='True'"
Environment="CE_DATABASE=$database_file"
ExecStart=$PWD/.venv/bin/gunicorn --bind $bind_address app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

  echo "Enabling service..."
  sudo systemctl enable uon-ce || return 1

  echo "Starting service..."
  sudo systemctl start uon-ce || return 1

  echo "Success!"
}

if [[ $# -eq 1 ]]; then
  main "$1"
else
  echo "Provide the URL of the database and no other arguments."
fi

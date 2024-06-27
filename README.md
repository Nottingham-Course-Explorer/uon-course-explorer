# UoN Course Explorer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m797149454-d093364e38df45d848992fe4)](https://stats.uptimerobot.com/GmxX1fWvAM)
![GitHub License](https://img.shields.io/github/license/Nottingham-Course-Explorer/uon-course-explorer)

[Flask](https://flask.palletsprojects.com/) app for browsing University of Nottingham modules.
Uses 23 lines of JavaScript and a cookie.
Made for Python 3.12.

## Development
```
git clone https://github.com/Nottingham-Course-Explorer/uon-course-explorer.git
cd uon-course-explorer
python -m venv .venv; source .venv/bin/activate
pip install -r requirements.txt
cd src
flask run
```
Set the `CE_DATABASE` environment variable to the path to your database file.

## Deployment
```
git clone https://github.com/Nottingham-Course-Explorer/uon-course-explorer.git
cd uon-course-explorer
bash deploy/deploy.sh [Database URL]
```
The deployment script downloads your database from the given URL and configures [Gunicorn](https://gunicorn.org/) on `127.0.0.1:5100`.

### Installing Caddy
```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

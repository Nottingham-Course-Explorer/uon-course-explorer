# UoN Course Explorer
[Flask](https://flask.palletsprojects.com/) app for browsing University of Nottingham modules.
Uses 23 lines of JavaScript and one cookie.

## Deploying
```
git clone https://github.com/Nottingham-Course-Explorer/uon-course-explorer.git
cd uon-course-explorer
bash deploy/deploy.sh
```
The deployment script configures [Gunicorn](https://gunicorn.org/) on `127.0.0.1:5100`.

## Installing Caddy
```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```
Included here for convenience.

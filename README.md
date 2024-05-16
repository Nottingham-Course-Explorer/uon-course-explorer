# UoN Course Explorer
[Flask](https://flask.palletsprojects.com/) app for browsing University of Nottingham modules.
Uses [HTMX](https://htmx.org/) and [Hyperscript](https://hyperscript.org/) in places to improve usability.

## Deploying
```
git clone https://github.com/Nottingham-Course-Explorer/uon-course-explorer.git
cd uon-course-explorer
bash deploy/deploy.sh
```
The deployment script configures [Gunicorn](https://gunicorn.org/) on `127.0.0.1:5100`.

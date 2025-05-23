from os import environ
from time import strftime
from urllib.parse import urlencode

from flask import Flask, render_template, g, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix

import api.search
from pages import index, staff, module

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.template_global()
def modify_parameters(**new_values) -> str:
    args = request.args.copy()

    for parameter, value in new_values.items():
        args[parameter] = value

    return f"{request.path}?{urlencode(args)}"


@app.teardown_appcontext
def close_db(exception) -> None:
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(error) -> (str, int):
    return render_template("404.jinja.html"), 404


@app.after_request
def add_security_headers(response: Response) -> Response:
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"

    timestamp = strftime("[%Y-%b-%d %H:%M]")
    logger.info(
        "%s %s %s %s %s %s",
        timestamp,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        response.status,
    )

    return response


app.url_map.strict_slashes = False
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.add_url_rule("/staff/<username>", view_func=staff.staff_page)
app.add_url_rule("/module/<code>", view_func=module.module_page)
app.add_url_rule("/random-module", view_func=module.random_module)
app.add_url_rule("/", view_func=index.index_page)
app.add_url_rule("/malaysia", view_func=index.index_page_malaysia)
app.add_url_rule("/china", view_func=index.index_page_china)

app.add_url_rule("/opensearch-suggestions", view_func=api.search.opensearch_suggestions)

handler = RotatingFileHandler("app.log", maxBytes=100000, backupCount=3)
logger = logging.getLogger("tdm")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if environ.get("CE_PROXY", "False") == "True":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1, x_prefix=1)

if __name__ == "__main__":
    app.run()

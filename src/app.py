from urllib.parse import urlencode

from flask import Flask, render_template, g, request
from werkzeug.middleware.proxy_fix import ProxyFix
from pathlib import Path

import index
import module
import staff
from os import environ

app = Flask(__name__)


@app.template_global()
def modify_parameters(**new_values):
    args = request.args.copy()
    
    for parameter, value in new_values.items():
        args[parameter] = value
    
    return f"{request.path}?{urlencode(args)}"


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html.jinja"), 404


@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"
    return response


app.url_map.strict_slashes = False
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.add_url_rule("/staff/<username>", view_func=staff.staff_page)
app.add_url_rule("/module/<code>", view_func=module.module_page)
app.add_url_rule("/find-module/<code>", view_func=module.find_module)
app.add_url_rule("/random-module", view_func=module.random_module)
app.add_url_rule("/", view_func=index.index_page)

if environ.get("CE_PROXY", "False") == "True":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1, x_prefix=1)

if __name__ == '__main__':
    app.run()

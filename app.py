import hashlib
import sqlite3
from random import randint

from flask import Flask, render_template, g, abort, request

app = Flask(__name__)
app.url_map.strict_slashes = False

DATABASE = "./modules.db"


def random_number():
    return randint(1000000, 9999999)


app.jinja_env.globals.update(random_number=random_number)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def with_names(result):
    return {column_name: result[i] for i, column_name in enumerate(result.keys())}


@app.route("/person/<username>")
def person(username: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        abort(404)
    return render_template("person.html.jinja", person=with_names(result))


@app.route("/module/<code>")
def module(code: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM modules WHERE code = ?", (code,))
    result = cursor.fetchone()
    if result is None:
        abort(404)
    conveners = [
        {"name": s.strip(), "username": result[10].split(",")[i]}
        for i, s in enumerate(result[6].split(","))
    ]
    public_token = hashlib.sha256(bytes(request.remote_addr, "utf-8")).hexdigest()
    return render_template("module.html.jinja",
                           module=with_names(result),
                           conveners=conveners,
                           public_token=public_token,
                           public_token_short=public_token[0:10])


@app.route("/")
def index():
    cursor = get_db().cursor()
    name_query = request.args.get("name") or ""
    cursor.execute("SELECT * FROM modules WHERE title like ?", (f"%{name_query}%",))
    results = cursor.fetchall()
    return render_template("index.html.jinja", results=results, name_query=name_query)


if __name__ == '__main__':
    app.run()

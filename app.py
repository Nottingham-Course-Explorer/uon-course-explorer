import hashlib
import sqlite3

from flask import Flask, render_template, g, abort, request

app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

DATABASE = "./modules.db"


def add_cols(result) -> dict[str, str] | None:
    return {column_name: result[i] for i, column_name in
            enumerate(result.keys())} if result is not None else None


def add_cols_list(result: list) -> list[dict[str, str]] | None:
    return [add_cols(i) for i in result] if result is not None else None


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html.jinja"), 404


@app.route("/person/<username>")
def person_page(username: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    person = add_cols(cursor.fetchone())
    if person is None:
        abort(404)
    return render_template("person.html.jinja", person=person)


@app.route("/module/<code>")
def module_page(code: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM modules WHERE code = ?", (code,))
    module = add_cols(cursor.fetchone())
    if module is None:
        abort(404)
    usernames = module["convener_usernames"].split(",")
    conveners = [
        {"name": s.strip(), "username": usernames[i]}
        for i, s in enumerate(module["conveners"].split(","))
    ]
    public_token = hashlib.sha256(bytes(request.remote_addr, "utf-8")).hexdigest()
    return render_template("module.html.jinja",
                           module=module,
                           conveners=conveners,
                           public_token=public_token,
                           public_token_short=public_token[0:10])


@app.route("/")
def index():
    cursor = get_db().cursor()
    name_query = request.args.get("name") or ""
    cursor.execute("SELECT * FROM modules WHERE title like ?", (f"%{name_query}%",))
    modules = add_cols_list(cursor.fetchall())

    level_query = request.args.get("level")

    semester_query = request.args.get("semester")

    return render_template("index.html.jinja",
                           modules=modules,
                           name_query=name_query,
                           level_query=level_query,
                           semester_query=semester_query)


if __name__ == '__main__':
    app.run()

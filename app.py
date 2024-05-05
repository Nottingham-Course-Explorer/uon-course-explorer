import hashlib
import sqlite3

from flask import Flask, render_template, g, abort, request
from urllib.parse import urlencode

app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

DATABASE = "./modules.db"

FEATURE_FLAGS = []


@app.template_global()
def modify_parameters(**new_values):
    args = request.args.copy()
    
    for parameter, value in new_values.items():
        args[parameter] = value
        
    return f"{request.path}?{urlencode(args)}"


def add_cols(result) -> dict[str, str] | None:
    return {column_name: result[i] for i, column_name in enumerate(result.keys())} if result is not None else None


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
    conveners = [{"name": s.strip(), "username": usernames[i]} for i, s in enumerate(module["conveners"].split(","))]
    
    public_token = hashlib.sha256(bytes(request.remote_addr, "utf-8")).hexdigest()
    
    return render_template("module.html.jinja", module=module, conveners=conveners, public_token=public_token,
                           public_token_short=public_token[0:10], feature_flags=FEATURE_FLAGS)


MODULES_PER_PAGE = 20


@app.route("/")
def index():
    name = request.args.get("name", "")
    level = request.args.get("level", "")
    semester = request.args.get("semester", "")
    
    parameters = [f"%{name}%"]
    terms = ""
    if level != "":
        terms += " AND level = ?"
        parameters.append(level)
    if semester != "":
        terms += " AND semesters LIKE ?"
        parameters.append(f"%{semester}%")
    
    cursor = get_db().cursor()
    
    # Count all results of query, without pagination
    count_query = f"SELECT COUNT(code) FROM modules WHERE title like ?{terms}"
    cursor.execute(count_query, parameters)
    count = cursor.fetchone()[0]
    
    # Calculate pagination
    pages = max(int((count + MODULES_PER_PAGE - 1) / MODULES_PER_PAGE), 1)
    page = max(min(request.args.get("page", 1, type=int), pages), 1)
    offset = (page - 1) * MODULES_PER_PAGE
    
    # Perform query with pagination
    query = f"SELECT * FROM modules WHERE title like ?{terms} ORDER BY title LIMIT {MODULES_PER_PAGE} OFFSET {offset}"
    cursor.execute(query, parameters)
    modules = add_cols_list(cursor.fetchall())
    
    return render_template("index.html.jinja", modules=modules, name_query=name, level_query=level,
                           semester_query=semester, page=page, pages=pages)


if __name__ == '__main__':
    app.run()

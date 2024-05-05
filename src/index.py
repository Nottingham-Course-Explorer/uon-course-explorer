from flask import request, render_template

from utils import get_db, add_column_names_list

MODULES_PER_PAGE = 20


def index_page():
    name = request.args.get("name", "")
    level = request.args.get("level", "")
    semester = request.args.get("semester", "")
    
    # Assemble SQL query
    parameters = [f"%{name}%"]
    terms = "WHERE title LIKE ? "
    if level != "":
        terms += "AND level = ? "
        parameters.append(level)
    if semester != "":
        terms += "AND semesters LIKE ? "
        parameters.append(f"%{semester}%")
    
    cursor = get_db().cursor()
    
    # Count all results of query without pagination
    query = f"SELECT COUNT(code) FROM modules {terms}"
    cursor.execute(query, parameters)
    count = cursor.fetchone()[0]
    
    # Calculate pagination
    pages = max(int((count + MODULES_PER_PAGE - 1) / MODULES_PER_PAGE), 1)
    page = max(min(request.args.get("page", 1, type=int), pages), 1)
    offset = (page - 1) * MODULES_PER_PAGE
    
    # Perform query with pagination
    query = (f"SELECT * FROM modules {terms}"
             f"ORDER BY title LIMIT {MODULES_PER_PAGE} OFFSET {offset}")
    cursor.execute(query, parameters)
    modules = add_column_names_list(cursor.fetchall())
    
    return render_template("index.html.jinja",
                           modules=modules,
                           name_query=name, level_query=level, semester_query=semester,
                           page=page, pages=pages)

import json
from datetime import timedelta

from flask import request, render_template, make_response

from tools import get_db, add_column_names_list

MODULES_PER_PAGE = 20
LAST_SCHOOL_COOKIE = "last_school"

with open("../search_options.json") as file:
    search_options = json.loads(file.read())
    LEVEL_OPTIONS = search_options["levels"]
    SEMESTER_OPTIONS = search_options["semesters"]
    SCHOOL_OPTIONS = search_options["schools"]


def index_page():
    title = request.args.get("title", "")
    level = request.args.get("level", "")
    semester = request.args.get("semester", "")
    school_cookie = request.cookies.get(LAST_SCHOOL_COOKIE, "")
    school = request.args.get("school",
                              school_cookie
                              if school_cookie in SCHOOL_OPTIONS else SCHOOL_OPTIONS[0])
    
    # Assemble SQL query
    parameters = [school]
    terms = "WHERE school = ?"
    if title != "":
        terms += "AND title LIKE ? "
        parameters.append(f"%{title}%")
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
    
    # Notes about data:
    # - Sometimes Target Students and Additional Requirements text are exactly the same.
    #   Maybe don't show Additional Requirements if this is the case.
    # - Sometimes there are no conveners listed.
    
    response = make_response(render_template("index.html.jinja",
                                             modules=modules,
                                             name_query=title,
                                             level_query=level, level_options=LEVEL_OPTIONS,
                                             semester_query=semester,
                                             semester_options=SEMESTER_OPTIONS,
                                             school_query=school, school_options=SCHOOL_OPTIONS,
                                             page=page, pages=pages))
    response.set_cookie(LAST_SCHOOL_COOKIE, school, max_age=timedelta(days=365))
    return response

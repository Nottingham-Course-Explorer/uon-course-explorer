import json
from datetime import timedelta

from flask import request, render_template, make_response, Response, url_for

from tools import get_db, add_column_names_list

MODULES_PER_PAGE = 20
LAST_SCHOOL_COOKIE = "last_school"

with open("../search_options.json") as file:
    SEARCH_OPTIONS = json.loads(file.read())


def index_page() -> Response:
    return index_page_sub("Nottingham", url_for("index_page"))


def index_page_malaysia() -> Response:
    return index_page_sub("Malaysia", url_for("index_page_malaysia"))


def index_page_china() -> Response:
    return index_page_sub("China", url_for("index_page_china"))


def index_page_sub(campus: str, campus_url: str) -> Response:
    search_options = SEARCH_OPTIONS[campus]
    school_options = search_options["schools"]
    level_options = search_options["levels"]
    semester_options = search_options["semesters"]

    title = request.args.get("title", "")
    level = request.args.get("level", "")
    semester = request.args.get("semester", "")
    school_cookie = request.cookies.get(LAST_SCHOOL_COOKIE, "")
    school = request.args.get(
        "school",
        school_cookie if school_cookie in school_options else school_options[0],
    )

    # Assemble SQL query
    parameters = [school, campus]
    terms = "WHERE school = ? AND campus = ?"
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
    query = (
        f"SELECT * FROM modules {terms}"
        f"ORDER BY title LIMIT {MODULES_PER_PAGE} OFFSET {offset}"
    )
    cursor.execute(query, parameters)
    modules = add_column_names_list(cursor.fetchall())

    response = make_response(
        render_template(
            "index.jinja.html",
            modules=modules,
            name_query=title,
            level_query=level,
            level_options=level_options,
            semester_query=semester,
            semester_options=semester_options,
            school_query=school,
            school_options=school_options,
            page=page,
            pages=pages,
            my_url=campus_url,
            campus=campus
        )
    )
    response.set_cookie(
        LAST_SCHOOL_COOKIE,
        school,
        max_age=timedelta(days=365),
        secure=True,
        httponly=True,
        samesite="Strict",
    )
    response.headers["Cache-Control"] = "max-age=3600"
    return response

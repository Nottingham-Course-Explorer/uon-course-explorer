import json

from flask import request, Response, url_for

from tools import get_db, add_column_names_list


def opensearch_suggestions():
    search_term = request.args.get("searchTerms", "")
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT * FROM modules WHERE title LIKE ? LIMIT 10", ("%" + search_term + "%",)
    )
    modules = add_column_names_list(cursor.fetchall())

    suggestion_texts = []
    description_texts = []
    urls = []

    for module in modules:
        suggestion_texts.append(module["title"])
        description_texts.append("Lorem ipsum dolor sit amet")
        urls.append("https://uoncourses.org/" + url_for("module_page", code=module["code"]))

    response = Response(
        json.dumps(
            [
                search_term,
                suggestion_texts,
                description_texts,
                urls
            ]
        )
    )
    response.headers["Content-Type"] = "application/x-suggestions+json; charset=utf-8"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response

import json

from flask import request, Response

from tools import get_db, add_column_names_list


def opensearch_suggestions():
    search_term = request.args.get("searchTerms", "")
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT * FROM modules WHERE campus='Nottingham' AND title LIKE ? LIMIT 10", ("%" + search_term + "%",)
    )
    modules = add_column_names_list(cursor.fetchall())

    response = Response(
        json.dumps(
            [
                search_term,
                [module["title"] for module in modules]
            ]
        )
    )
    response.headers["Content-Type"] = "application/x-suggestions+json; charset=utf-8"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response

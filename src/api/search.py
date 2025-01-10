from flask import request, Response

from tools import get_db, add_column_names_list


def opensearch_suggestions():
    search_terms = request.args.get("search_terms", "")
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT * FROM modules WHERE title LIKE ?", ("%" + search_terms + "%",)
    )
    modules = add_column_names_list(cursor.fetchall())

    response = Response(
        """["test", ["Just! Stop using Makefile", "What's new in Django 3.2 LTS", "Django Plaintext Password", "Temperature & Humidity Sensor with ESPHome", "State of the Server 2024"]]"""
    )
    response.headers["Content-Type"] = "application/x-suggestions+json; charset=utf-8"

    return response

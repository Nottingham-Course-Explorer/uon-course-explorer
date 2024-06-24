from datetime import datetime, timezone

from flask import abort, render_template, make_response, Response

from tools import get_db, add_column_names, add_column_names_list


def staff_page(username: str = None) -> Response:
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    staff = add_column_names(cursor.fetchone())

    if staff is None:
        abort(404)

    cursor.execute(
        "SELECT code, title FROM modules JOIN convenes ON code = module_code "
        "WHERE convenes.staff_username = ?",
        (username,),
    )
    convened_modules = add_column_names_list(cursor.fetchall())

    cursor.execute(
        "SELECT DISTINCT username, salutation, forename, surname FROM staff "
        "JOIN convenes ON username = staff_username WHERE module_code IN"
        "(SELECT module_code FROM convenes WHERE staff_username = ?) AND staff_username != ?",
        (username, username),
    )
    colleagues = add_column_names_list(cursor.fetchall())

    cursor.execute(
        "SELECT name FROM unknown_conveners WHERE module_code IN"
        "(SELECT module_code FROM convenes WHERE staff_username = ?)",
        (username,),
    )
    unknown_colleagues = add_column_names_list(cursor.fetchall())

    crawl_time = datetime.fromtimestamp(
        int(staff["crawl_time"]), timezone.utc
    ).strftime("%d/%m/%Y")

    response = make_response(
        render_template(
            "staff.html.jinja",
            staff=staff,
            modules=convened_modules,
            colleagues=colleagues,
            unknown_colleagues=unknown_colleagues,
            crawl_time=crawl_time,
        )
    )
    response.headers["Cache-Control"] = "max-age=3600"
    return response

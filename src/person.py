from flask import abort, render_template

from utils import get_db, add_column_names


def person_page(username: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    person = add_column_names(cursor.fetchone())
    
    if person is None:
        abort(404)
    
    return render_template("person.html.jinja", person=person)

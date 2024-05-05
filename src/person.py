from flask import abort, render_template

from utils import get_db, add_cols


def person_page(username: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    person = add_cols(cursor.fetchone())
    
    if person is None:
        abort(404)
    
    return render_template("person.html.jinja", person=person)

from datetime import datetime, timezone

from flask import abort, render_template

from utils import get_db, add_column_names


def staff_page(username: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    staff = add_column_names(cursor.fetchone())
    
    if staff is None:
        abort(404)
    
    crawl_time = datetime.fromtimestamp(int(staff["crawl_time"]), timezone.utc).strftime("%d/%m/%Y")
    
    return render_template("staff.html.jinja", staff=staff, crawl_time=crawl_time)

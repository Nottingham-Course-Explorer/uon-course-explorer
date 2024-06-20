from datetime import datetime, timezone

from flask import abort, render_template

from tools import get_db, add_column_names, add_column_names_list


def staff_page(username: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
    staff = add_column_names(cursor.fetchone())

    cursor.execute("SELECT code, title FROM modules WHERE convener_usernames LIKE ?", (f"%{staff['username']}%",))
    convened_modules = add_column_names_list(cursor.fetchall())
    print(convened_modules)
    
    if staff is None:
        abort(404)
    
    crawl_time = datetime.fromtimestamp(int(staff["crawl_time"]), timezone.utc).strftime("%d/%m/%Y")
    
    return render_template("staff.html.jinja", staff=staff, modules=convened_modules, crawl_time=crawl_time)

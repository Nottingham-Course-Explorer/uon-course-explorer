from flask import abort, render_template

from constants import FEATURE_FLAGS
from utils import add_column_names, get_db


def module_page(code: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM modules WHERE code = ?", (code,))
    module = add_column_names(cursor.fetchone())
    
    if module is None:
        abort(404)
    
    convener_usernames = module["convener_usernames"].split(",")
    conveners = [{"name": s.strip(), "username": convener_usernames[i]} for i, s in
                 enumerate(module["conveners"].split(","))]
    
    # public_token = sha256(bytes(request.remote_addr, "utf-8")).hexdigest()
    
    return render_template("module.html.jinja",
                           module=module,
                           conveners=conveners,
                           # public_token=public_token,
                           # public_token_short=public_token[0:10],
                           feature_flags=FEATURE_FLAGS)

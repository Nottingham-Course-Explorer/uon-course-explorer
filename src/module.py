from datetime import datetime, timezone

from flask import abort, render_template

from config import FEATURE_FLAGS
from utils import add_column_names, get_db, parse_table


def format_class(class_: list[str]) -> str:
    class_type, number, every, duration = class_
    duration = duration.replace("hours", "hour").replace(" ", "-")
    class_type = class_type.lower()
    if number == "1 week":
        return f"One {duration} {class_type}"
    every = every.replace("1 week", "week")
    return f"{duration} {class_type} every {every} for {number}"


def module_page(code: str = None):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM modules WHERE code = ?", (code,))
    module = add_column_names(cursor.fetchone())
    
    if module is None:
        abort(404)
    
    convener_usernames = module["convener_usernames"].split(",")
    conveners = [] if module["conveners"] == "" else [
        {"name": s.strip(), "username": convener_usernames[i]} for i, s in
        enumerate(module["conveners"].split(","))]
    
    classes = [format_class(class_) for class_ in parse_table(module["classes"], 4)]
    assessment = parse_table(module["assessment"], 5)
    for row in assessment:
        # Format weight
        row[1] = f"{int(float(row[1]))}%" if row[1].strip() != "" else ""
    crawl_time = datetime.fromtimestamp(int(module["crawl_time"]), timezone.utc).strftime(
        "%d/%m/%Y")
    
    # public_token = sha256(bytes(request.remote_addr, "utf-8")).hexdigest()
    
    return render_template("module.html.jinja",
                           module=module,
                           conveners=conveners,
                           classes=classes,
                           assessment=assessment,
                           crawl_time=crawl_time,
                           # public_token=public_token,
                           # public_token_short=public_token[0:10],
                           feature_flags=FEATURE_FLAGS)

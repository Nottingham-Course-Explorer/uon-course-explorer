from datetime import datetime, timezone

from flask import abort, render_template

from config import FEATURE_FLAGS
from utils import add_column_names, get_db, parse_table, digit_to_word


def format_class(class_: list[str]) -> str:
    class_type, number, per_week_str, duration = class_
    duration = duration.replace("hours", "hour").replace(" ", "-")
    class_type = class_type.lower()
    if number == "1 week":
        return f"One {duration} {class_type}"
    per_week = int(per_week_str.split(" ")[0])
    return (f"{digit_to_word(per_week).title()} {duration} "
            f"{class_type}{"s" if per_week > 1 else ""} per week for {number}")


def format_assessment(assessment_: list[str]) -> str:
    title, weight, type_, duration, requirements = assessment_
    weight = f"{int(float(weight))}%" if weight.strip() else ""
    duration_str = f" ({duration.replace("Hr", "-hour")})" if duration.strip() else ""
    return f"{weight} {title}{duration_str}: {requirements}"


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
    assessments = [format_assessment(assessment) for assessment in
                   parse_table(module["assessment"], 5)]
    crawl_time = datetime.fromtimestamp(int(module["crawl_time"]), timezone.utc).strftime(
        "%d/%m/%Y")
    
    # public_token = sha256(bytes(request.remote_addr, "utf-8")).hexdigest()
    
    return render_template("module.html.jinja",
                           module=module,
                           conveners=conveners,
                           classes=classes,
                           assessments=assessments,
                           crawl_time=crawl_time,
                           # public_token=public_token,
                           # public_token_short=public_token[0:10],
                           feature_flags=FEATURE_FLAGS)

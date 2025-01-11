import string
from datetime import datetime, timezone

from flask import abort, render_template, url_for, redirect, make_response, Response
from num2words import num2words

from config import FEATURE_FLAGS
from tools import (
    add_column_names,
    get_db,
    parse_table,
    add_column_names_list,
    make_links_clickable,
)


def module_page(code: str = None) -> Response:
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM modules WHERE code = ?", (code,))
    module = add_column_names(cursor.fetchone())

    if module is None:
        abort(404)

    # Get known conveners
    cursor.execute(
        "SELECT username, salutation, forename, surname FROM staff "
        "JOIN convenes ON username = staff_username WHERE module_code = ?",
        (code,),
    )
    known_conveners = add_column_names_list(cursor.fetchall())

    # Get unknown conveners
    cursor.execute("SELECT name FROM unknown_conveners WHERE module_code = ?", (code,))
    unknown_conveners = add_column_names_list(cursor.fetchall())

    # Make links clickable
    module["summary"] = make_links_clickable(module["summary"])
    module["learning_outcomes"] = make_links_clickable(module["learning_outcomes"])
    # Format classes
    classes = [format_class(*class_) for class_ in parse_table(module["classes"], 4)]
    # Format assessments
    assessments = [
        format_assessment(*assessment)
        for assessment in parse_table(module["assessment"], 5)
    ]
    # Format co_requisites
    co_requisites = [
        co_requisite for co_requisite in parse_table(module["co_requisites"], 2)
    ]
    # Not collected yet.
    # prerequisites = [
    #    prerequisite for prerequisite in parse_table(module["prerequisites"], 2)
    # ]

    # Format crawl time
    crawl_time = datetime.fromtimestamp(
        int(module["crawl_time"]), timezone.utc
    ).strftime("%d/%m/%Y")

    response = make_response(
        render_template(
            "module.jinja.html",
            module=module,
            known_conveners=known_conveners,
            unknown_conveners=unknown_conveners,
            co_requisites=co_requisites,
            # prerequisites=prerequisites,
            classes=classes,
            assessments=assessments,
            crawl_time=crawl_time,
            feature_flags=FEATURE_FLAGS,
        )
    )

    response.headers["Cache-Control"] = "max-age=300"
    return response


def random_module() -> Response:
    cursor = get_db().cursor()
    cursor.execute("SELECT code FROM modules ORDER BY RANDOM() LIMIT 1")
    module = add_column_names(cursor.fetchone())
    if module is None:
        abort(404)
    return redirect(url_for("module_page", code=module["code"]))


def format_class(class_type: str, weeks: str, per_week_str: str, duration: str) -> str:
    duration = (
        (
            duration.replace("and ", "")
            .replace("hours", "hour")
            .replace("minutes", "minute")
            .replace(" ", "-")
        )
        + " "
        if duration != ""
        else ""
    )
    if weeks == "1 week":
        return f"One {duration}{class_type.lower()}"
    per_week = int(per_week_str.split(" ")[0]) if per_week_str else 1
    return f"{string.capwords(num2words(per_week))} {duration}{class_type.lower()}{"s" if per_week > 1 else ""} each week for {weeks}"


def format_assessment(
    title: str, weight: str, type_: str, duration: str, requirements: str
) -> str:
    weight = f"{int(float(weight))}% " if weight.strip() else ""
    if duration.strip():
        duration_str = (
            " ("
            + (
                duration.replace("Hr", "-hour")
                .replace("Mins", "-minute")
                .replace(" ", "-")
            )
            + ")"
        )
    else:
        duration_str = ""
    requirements_str = ": " + requirements if requirements else ""
    return weight + title + duration_str + requirements_str

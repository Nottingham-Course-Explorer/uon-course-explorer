import json
import sqlite3
import sys

db = sqlite3.connect(sys.argv[1])
cursor = db.cursor()


def search_options(campus: str) -> dict:
    cursor.execute(
        "SELECT DISTINCT school FROM modules WHERE campus=? ORDER BY school", (campus,)
    )
    schools = [i[0] for i in cursor.fetchall()]

    cursor.execute(
        "SELECT DISTINCT level FROM modules WHERE campus=? ORDER BY level", (campus,)
    )
    levels = [str(i[0]) for i in cursor.fetchall()]

    cursor.execute(
        "SELECT DISTINCT semesters FROM modules WHERE campus=? ORDER BY semesters",
        (campus,),
    )
    semesters_entries = [i[0] for i in cursor.fetchall()]
    semesters = []
    for entry in semesters_entries:
        semesters += entry.split(", ")
    semesters = sorted(set(semesters))

    return {"schools": schools, "levels": levels, "semesters": semesters}


out = {campus: search_options(campus) for campus in ["Nottingham", "China", "Malaysia"]}

with open(sys.argv[2], "w") as file:
    file.write(json.dumps(out, indent=4))

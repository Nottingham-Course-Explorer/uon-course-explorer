import json
import sqlite3

from config import DATABASE

db = sqlite3.connect(DATABASE)
cursor = db.cursor()

cursor.execute("SELECT DISTINCT school FROM modules ORDER BY school")
schools = [i[0] for i in cursor.fetchall()]

cursor.execute("SELECT DISTINCT level FROM modules ORDER BY level")
levels = [str(i[0]) for i in cursor.fetchall()]

cursor.execute("SELECT DISTINCT semesters FROM modules ORDER BY semesters")
semesters_entries = [i[0] for i in cursor.fetchall()]
semesters = []
for entry in semesters_entries:
    semesters += entry.split(", ")

with open("../search_options.json", "w") as file:
    file.write(json.dumps({
        "schools": schools,
        "levels": levels,
        "semesters": sorted(set(semesters))
    }))

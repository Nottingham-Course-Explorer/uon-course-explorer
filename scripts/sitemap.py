import sqlite3
import sys


def module_url(code):
    return f"https://uoncourses.org/module/{code}\n"


lines = []

db = sqlite3.connect(sys.argv[1])
cursor = db.cursor()

cursor.execute("SELECT code FROM modules")
results = cursor.fetchall()

for module in results:
    module_code = module[0]
    if module_code != "":
        lines.append(module_url(module_code))

with open("sitemap.txt", "w") as f:
    f.writelines(lines)

db.commit()
db.close()

print(f"Wrote {len(lines)} URLs.")

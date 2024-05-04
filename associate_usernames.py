import sqlite3
from functools import cache

DATABASE = "./modules.db"
SALUTATIONS = ["Miss", "Mrs", "Mr", "Ms", "Dr", "Mx", "Prof", "Prosir", "Revdr", "Revrd", "Dame", "Baron"]

db = sqlite3.connect(DATABASE)

cursor = db.cursor()

cursor.execute("SELECT code, conveners FROM modules")
results = cursor.fetchall()


def one_or_none(_results):
    count = len(_results)
    if count == 1:
        return _results[0]
    elif count > 1:
        print(f"Multiple ({count}) results found...")
        return None
    else:
        return None


@cache
def lookup(name: str):
    # Mr John Smith
    # Mr John Beckett Smith
    # John Smith
    # John Beckett Smith
    first_rest = name.split(" ", 1)
    first = first_rest[0]
    # first = Mr | John
    has_salutation = first in SALUTATIONS
    if has_salutation:
        # salutation = first
        name = first_rest[1]
    name = name.replace("_", " ").title()
    forename, surname = name.split(" ", 1)
    middle: bool = len(surname.split(" ")) > 1
    cursor.execute("SELECT username FROM staff WHERE forename = ? AND surname = ?", (forename, surname))
    result = one_or_none(cursor.fetchall())
    
    if result is None and middle:
        print(f"Can't find username for {forename} | {surname}, trying [-1] of surname...")
        surname = surname.split(" ")[-1]
        cursor.execute("SELECT username FROM staff WHERE forename = ? AND surname = ?", (forename, surname))
        result = one_or_none(cursor.fetchall())
    if result is None:
        print(f"ERROR: Couldn't find {forename} | {surname}")
        return "NULL"
    else:
        return result[0]


for row in results:
    module_code = row[0]
    names = row[1]
    convener_usernames = [lookup(s.strip()) if s.strip() != "" else "" for s in names.split(",")]
    cursor.execute("UPDATE modules SET convener_usernames = ? WHERE code = ?",
                   (",".join(convener_usernames), module_code))

db.commit()
db.close()

print("Done.")

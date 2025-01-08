import sqlite3
from functools import cache
import sys
from typing import TypeVar

"""This script goes through all the modules and attempts to associate the names of the module
conveners with the names obtained from the Staff Lookup API, and writes their usernames.

- Some staff names in modules are not in the Staff Lookup database.
- Some staff names include varying numbers of middle names, or different salutations.
- Some staff names in modules do not provide enough middle names to determine which of multiple
Staff Lookup results are the mentioned person. We don't guess in this case.

Usage:
- Run `sqlite3 modules.db ".read scripts/setup_conveners.sql"` first.
- `python associate_conveners.py modules.db`
"""

SALUTATIONS = [
    "Miss",
    "Mrs",
    "Mr",
    "Ms",
    "Dr",
    "Mx",
    "Prof",
    "Prosir",
    "Revdr",
    "Revrd",
    "Dame",
    "Baron",
]

db = sqlite3.connect(sys.argv[1])
cursor = db.cursor()

T = TypeVar("T")

associated_total = 0
not_associated_total = 0


def one_or_none(_results: list[T]) -> T | None:
    count = len(_results)
    if count == 1:
        return _results[0]
    elif count > 1:
        print(f"Multiple ({count}) results found...")
        return None
    else:
        return None


@cache
def lookup(full_name: str) -> str | None:
    global associated_total, not_associated_total
    # "Mr John Smith"
    # "Mr John Beckett Smith"
    # "John Smith"
    # "John Beckett Smith"
    first_rest = full_name.split(" ", 1)  # ["John", "Smith"] | ["Mr", "John Smith"]
    first = first_rest[0]  # "John" | "Mr"
    if first in SALUTATIONS:
        full_name = first_rest[1]
    full_name = full_name.replace("_", " ").title()
    forename, surname = full_name.split(" ", 1)
    middle: bool = len(surname.split(" ")) > 1
    cursor.execute(
        "SELECT username FROM staff WHERE forename = ? AND surname = ?",
        (forename, surname),
    )
    staff = one_or_none(cursor.fetchall())

    if staff is None and middle:
        print(
            f"Can't find username for {forename} | {surname}, trying [-1] of surname..."
        )
        surname = surname.split(" ")[-1]
        cursor.execute(
            "SELECT username FROM staff WHERE forename = ? AND surname = ?",
            (forename, surname),
        )
        staff = one_or_none(cursor.fetchall())
    if staff is None:
        print(f"Couldn't find `{forename}` `{surname}`.")
        not_associated_total += 1
        return None
    else:
        print(f"Found {forename} {surname}.")
        associated_total += 1
        return staff[0]


cursor.execute("SELECT code, conveners FROM modules")
results = cursor.fetchall()

for row in results:
    module_code = row[0]
    convener_names = row[1]

    for name in convener_names.split(","):
        if name.strip() == "":
            continue

        username = lookup(name.strip())

        if username is not None:
            cursor.execute(
                "INSERT OR IGNORE INTO convenes VALUES (?, ?)", (username, module_code)
            )
        else:
            cursor.execute(
                "INSERT OR IGNORE INTO unknown_conveners VALUES (?, ?)",
                (name, module_code),
            )

db.commit()
db.close()

print(
    f"\nDone. Found {associated_total} people, couldn't find {not_associated_total}.\n"
)

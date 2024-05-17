import sqlite3
from sqlite3 import Row, Connection

from flask import g

from config import DATABASE


def add_column_names(result: Row | None) -> dict[str, str] | None:
    """
    Transforms a result dictionary from {0: "value"} to {"column": "value"}
    """
    return None if result is None else {column_name: result[i] for i, column_name in
                                        enumerate(result.keys())}


def add_column_names_list(results: list[Row] | None) -> list[dict[str, str]] | None:
    """
    Transforms a list of result dictionaries from {0: "value"} to {"column": "value"}
    """
    return None if results is None else [add_column_names(result) for result in results]


def parse_table(text: str, columns: int) -> list[list[str]]:
    if text == "":
        return []
    items = text.split("|")
    return [items[i:i + columns] for i in range(0, len(items), columns)]


def get_db() -> Connection:
    """
    Try to get an existing database connection, otherwise open one.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = Row
    return db


def digit_to_word(num: int) -> str:
    return {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }[num]

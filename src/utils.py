import sqlite3

from flask import g

from constants import DATABASE


def add_cols(result: dict[int, str] | None) -> dict[str, str] | None:
    return None if result is None else {column_name: result[i] for i, column_name in
                                        enumerate(result.keys())}


def add_cols_list(results: list[dict[int, str]] | None) -> list[dict[str, str]] | None:
    return None if results is None else [add_cols(result) for result in results]


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

import sqlite3

from flask import g

from config import DATABASE


def add_cols(result) -> dict[str, str] | None:
    return {column_name: result[i] for i, column_name in enumerate(result.keys())} if result is not None else None


def add_cols_list(result: list) -> list[dict[str, str]] | None:
    return [add_cols(i) for i in result] if result is not None else None


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

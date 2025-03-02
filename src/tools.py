import sqlite3
from os import environ
from sqlite3 import Row, Connection
import re
from urllib.parse import urlparse

from flask import g

URL_REGEX = r'(?<!["\'>])\bhttps?:\/\/[^\s"\'<>\)]+'


def make_links_clickable(html: str) -> str:
    def wrap_with_anchor(match):
        url = urlparse(match.group()).geturl()
        return f'<a href="{url}">{url}</a>'

    return re.sub(URL_REGEX, wrap_with_anchor, html)


def add_column_names(result: Row | None) -> dict[str, str] | None:
    """
    Transforms a result dictionary from {0: "value"} to {"column": "value"}
    """
    return (
        None
        if result is None
        else {column_name: result[i] for i, column_name in enumerate(result.keys())}
    )


def add_column_names_list(results: list[Row] | None) -> list[dict[str, str]] | None:
    """
    Transforms a list of result dictionaries from {0: "value"} to {"column": "value"}
    """
    return None if results is None else [add_column_names(result) for result in results]


def parse_table(text: str, columns: int) -> list[list[str]]:
    if text == "":
        return []
    items = text.split("|")
    return [items[i : i + columns] for i in range(0, len(items), columns)]


def get_db() -> Connection:
    """
    Try to get an existing database connection, otherwise open one.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(environ["CE_DATABASE"])
        db.row_factory = Row
    return db

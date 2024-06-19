import sqlite3

from src.module import format_assessment, format_class
from tools import parse_table


def test_format_assessment():
    assert format_assessment(
        "Coursework 1",
        "25.00",
        "Coursework",
        "",
        "Programming exercises."
    ) == "25% Coursework 1: Programming exercises."
    assert format_assessment(
        "Exam 1",
        "75.00",
        "Written (in-person)",
        "2Hr 30Mins",
        "Written examination."
    ) == "75% Exam 1 (2-hour-30-minute): Written examination."
    assert format_assessment(
        "Participation",
        "100.00",
        "Participation",
        "",
        ""
    ) == "100% Participation"


def test_format_assessment_all():
    db = sqlite3.connect("../modules.db")
    cursor = db.cursor()
    cursor.execute("SELECT assessment FROM MODULES")
    for row in cursor.fetchall():
        for assessment in parse_table(row[0], 5):
            print(format_assessment(*assessment))


def test_format_class_all():
    db = sqlite3.connect("../modules.db")
    cursor = db.cursor()
    cursor.execute("SELECT classes FROM MODULES")
    for row in cursor.fetchall():
        for class_ in parse_table(row[0], 4):
            print(format_class(*class_))

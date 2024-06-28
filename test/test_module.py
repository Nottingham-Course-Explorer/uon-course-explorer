import sqlite3

import requests

from pages.module import format_assessment, format_class
from tools import parse_table

from os import environ


def test_format_assessment():
    assert (
        format_assessment(
            "Coursework 1", "25.00", "Coursework", "", "Programming exercises."
        )
        == "25% Coursework 1: Programming exercises."
    )
    assert (
        format_assessment(
            "Exam 1",
            "75.00",
            "Written (in-person)",
            "2Hr 30Mins",
            "Written examination.",
        )
        == "75% Exam 1 (2-hour-30-minute): Written examination."
    )
    assert (
        format_assessment("Participation", "100.00", "Participation", "", "")
        == "100% Participation"
    )


def test_format_class():
    assert (
        format_class("Lecture", "11 weeks", "1 week", "1 hours and 30 minutes")
        == "One 1-hour-30-minute lecture per week for 11 weeks"
    )
    assert (
        format_class("Seminar", "10 weeks", "2 week", "2 hours")
        == "Two 2-hour seminars per week for 10 weeks"
    )
    assert (
        format_class("Lecture", "9 weeks", "35 week", "1 hour")
        == "Thirty-five 1-hour lectures per week for 9 weeks"
    )


def test_format_assessment_all():
    db = sqlite3.connect(environ["CE_DATABASE"])
    cursor = db.cursor()
    cursor.execute("SELECT assessment FROM MODULES")
    for row in cursor.fetchall():
        for assessment in parse_table(row[0], 5):
            print(format_assessment(*assessment))


def test_format_class_all():
    db = sqlite3.connect(environ["CE_DATABASE"])
    cursor = db.cursor()
    cursor.execute("SELECT classes FROM MODULES")
    for row in cursor.fetchall():
        for class_ in parse_table(row[0], 4):
            print(format_class(*class_))


def local_module_url(code):
    return f"http://127.0.0.1:5000/module/{code}"


def test_ok_responses():
    db = sqlite3.connect(environ["CE_DATABASE"])
    cursor = db.cursor()
    cursor.execute("SELECT code FROM modules")
    for module in cursor.fetchall():
        module_code = module[0]
        if module_code != "":
            r = requests.get(local_module_url(module_code))
            assert r.status_code == 200

"""
Test for the trainings script.

@author: Fabio
"""
import datetime
import pytest
from src.trainings import Training, create_event

EVENT = {
    "summary": "Hello world",
    "description": "Created using Python",
    "start": {
        "date": "2000-02-01",
    },
    "end": {
        "date": "2000-02-01",
    },
}


@pytest.fixture
def training():
    training = Training(1, 2, 2000)
    return training

def test_day(training):
    assert training.day == 1

def test_month(training):
    assert training.month == 2

def test_year(training):
    assert training.year == 2000

def test_create_event():
    summary = "Hello world"
    start = datetime.date(year=2000, month=2, day=1).isoformat()
    day = 1
    week = 1
    assert create_event(summary, start, day, week) == EVENT

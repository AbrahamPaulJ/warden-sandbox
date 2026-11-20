from datetime import datetime, timezone

import pytest

from duedate import days_left, format_due, is_overdue, parse_utc


def test_parse_utc_accepts_z():
    assert parse_utc("2026-11-30T18:00:00Z").hour == 18


def test_parse_utc_rejects_naive():
    with pytest.raises(ValueError):
        parse_utc("2026-11-30T18:00:00")


def test_format_due_utc():
    assert format_due("2026-11-30T18:00:00Z") == "2026-11-30"


def test_format_due_local_date():
    # 18:00 UTC on Nov 30 is already Dec 1 in Auckland (UTC+13 in summer).
    assert format_due("2026-11-30T18:00:00Z", tz="Pacific/Auckland") == "2026-12-01"


def test_format_due_behind_utc():
    # 03:00 UTC on Dec 1 is still Nov 30 in New York.
    assert format_due("2026-12-01T03:00:00Z", tz="America/New_York") == "2026-11-30"


def test_days_left():
    now = datetime(2026, 11, 28, 18, 0, tzinfo=timezone.utc)
    assert days_left("2026-11-30T18:00:00Z", now) == 2


def test_is_overdue():
    now = datetime(2026, 12, 1, tzinfo=timezone.utc)
    assert is_overdue("2026-11-30T18:00:00Z", now)
    assert not is_overdue("2026-12-02T00:00:00Z", now)

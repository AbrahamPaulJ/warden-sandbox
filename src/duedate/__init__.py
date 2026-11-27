"""Due-date helpers for a small task tracker.

Deadlines are stored as UTC ISO-8601 stamps ("2026-11-30T18:00:00Z") and shown to
people as calendar dates in their team's time zone.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

__all__ = ["parse_utc", "format_due", "days_left", "is_overdue"]


def parse_utc(stamp: str) -> datetime:
    """Parse a UTC ISO-8601 stamp. A trailing "Z" or "+00:00" is required."""
    if not (stamp.endswith("Z") or stamp.endswith("+00:00")):
        raise ValueError(f"not a UTC stamp: {stamp!r}")
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(timezone.utc)


def format_due(stamp: str, tz: str = "UTC") -> str:
    """Format a UTC deadline as a local calendar date (YYYY-MM-DD) in time zone `tz`."""
    return parse_utc(stamp).date().isoformat()


def days_left(stamp: str, now: datetime) -> int:
    """Whole days from `now` until the deadline (negative once it has passed)."""
    delta = parse_utc(stamp) - now.astimezone(timezone.utc)
    return delta // timedelta(days=1)


def is_overdue(stamp: str, now: datetime) -> bool:
    return parse_utc(stamp) <= now.astimezone(timezone.utc)

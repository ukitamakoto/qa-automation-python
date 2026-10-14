"""SQL checks for a legacy-to-normalized booking migration.

Each file in sql/checks/ returns the rows that break one rule, so an empty result means the rule holds.
"""

import sqlite3
from pathlib import Path

import pytest

SQL = Path(__file__).resolve().parents[2] / "sql"
KNOWN = {
    "every_legacy_booking_is_migrated": pytest.mark.xfail(
        reason="BUG-013: bookings whose legacy e-mail has capitals are dropped"
    ),
    "totals_are_preserved_to_the_cent": pytest.mark.xfail(
        reason="BUG-014: float conversion loses a cent on some prices"
    ),
    "checkout_is_after_checkin": pytest.mark.xfail(
        reason="BUG-015: impossible stays are migrated without being flagged"
    ),
}


@pytest.fixture(scope="module")
def db():
    con = sqlite3.connect(":memory:")
    con.executescript((SQL / "legacy.sql").read_text(encoding="utf-8"))
    con.executescript((SQL / "migration.sql").read_text(encoding="utf-8"))
    yield con
    con.close()


CHECKS = [
    pytest.param(f, id=f.stem, marks=[KNOWN[f.stem]] if f.stem in KNOWN else [])
    for f in sorted((SQL / "checks").glob("*.sql"))
]


@pytest.mark.parametrize("check", CHECKS)
def test_check_returns_no_rows(db, check):
    rows = db.execute(check.read_text(encoding="utf-8")).fetchall()
    assert rows == [], f"{len(rows)} row(s) break the rule: {rows}"

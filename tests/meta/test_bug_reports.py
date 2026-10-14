"""Every xfail names an existing bug report, and every bug report is reproduced by a test."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REASON = re.compile(r'reason="(BUG-\d{3}): ')


def _test_sources():
    return [f for f in (ROOT / "tests").rglob("test_*.py") if f.parent.name != "meta"]


def referenced_bugs() -> set[str]:
    return {bug for f in _test_sources() for bug in REASON.findall(f.read_text(encoding="utf-8"))}


def test_every_xfail_has_a_bug_reason():
    for f in _test_sources():
        text = f.read_text(encoding="utf-8")
        assert text.count("xfail(") == len(REASON.findall(text)), f"xfail without a BUG reason in {f.name}"


def test_every_xfail_reason_names_an_existing_bug_report():
    missing = sorted(b for b in referenced_bugs() if not (ROOT / "docs/bugs" / f"{b}.md").exists())
    assert not missing, f"xfail reasons without a report: {missing}"


def test_every_bug_report_is_reproduced_by_a_test():
    reports = {p.stem for p in (ROOT / "docs/bugs").glob("BUG-*.md")}
    assert reports == referenced_bugs()

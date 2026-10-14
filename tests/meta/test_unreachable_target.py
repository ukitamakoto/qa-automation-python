"""When Restful-Booker is down, the API tests must say so instead of failing obscurely."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_api_tests_report_an_unreachable_target_clearly():
    env = os.environ | {"BOOKER_URL": "http://127.0.0.1:9"}
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/api/test_auth.py", "-x", "-q", "-p", "no:cacheprovider"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode != 0
    assert "Restful-Booker is unreachable at http://127.0.0.1:9" in result.stdout

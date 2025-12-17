import subprocess
import json
import pandas as pd
import tempfile
import os

def extract_features_from_code(code: str, file_name: str = "temp.py"):

    # Save code to a temporary file
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, file_name)
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(code)

    bandit_result = subprocess.run(
        ["bandit", "-f", "json", "-q", tmp_path],
        capture_output=True, text=True
    )
    bandit_json = {}
    if bandit_result.stdout:
        try:
            bandit_json = json.loads(bandit_result.stdout)
        except Exception:
            bandit_json = {}

    bandit_issues = bandit_json.get("results", [])
    bandit_rules = [issue.get("test_id") for issue in bandit_issues]

    pylint_result = subprocess.run(
        ["pylint", "--output-format=json", tmp_path],
        capture_output=True, text=True
    )
    pylint_json = []
    if pylint_result.stdout:
        try:
            pylint_json = json.loads(pylint_result.stdout)
        except Exception:
            pylint_json = []

    pylint_rules = [issue.get("message-id") for issue in pylint_json]

    features = {
        "pylint_total": len(pylint_json),
        "pylint_error": sum(1 for i in pylint_json if i.get("type") == "error"),
        "pylint_warning": sum(1 for i in pylint_json if i.get("type") == "warning"),
        "pylint_convention": sum(1 for i in pylint_json if i.get("type") == "convention"),
        "pylint_refactor": sum(1 for i in pylint_json if i.get("type") == "refactor"),
        "bandit_total": len(bandit_issues),
        "bandit_high": sum(1 for i in bandit_issues if i.get("issue_severity") == "HIGH"),
        "bandit_medium": sum(1 for i in bandit_issues if i.get("issue_severity") == "MEDIUM"),
        "bandit_low": sum(1 for i in bandit_issues if i.get("issue_severity") == "LOW"),
    }

    # Clean up temp file
    try:
        os.remove(tmp_path)
        os.rmdir(tmp_dir)
    except Exception:
        pass

    # Return DataFrame + rule IDs
    return pd.DataFrame([features]), bandit_rules + pylint_rules

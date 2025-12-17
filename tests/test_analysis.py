import pytest
import pandas as pd
from api import analysis

def test_extract_features_simple_code(tmp_path):
    # Create a simple Python file
    code = "print('Hello world')"
    file_name = tmp_path / "hello.py"

    # Run feature extraction
    features, rule_ids = analysis.extract_features_from_code(code, file_name.name)

    # Assertions
    assert isinstance(features, pd.DataFrame)
    assert "pylint_total" in features.columns
    assert "bandit_total" in features.columns
    assert isinstance(rule_ids, list)

def test_extract_features_with_bug(tmp_path):
    # Code with an obvious issue (exec usage)
    code = "exec('print(123)')"
    file_name = tmp_path / "buggy.py"

    features, rule_ids = analysis.extract_features_from_code(code, file_name.name)

    # Should detect at least one Bandit rule
    assert features["bandit_total"].iloc[0] >= 1
    assert any(r.startswith("B") for r in rule_ids)

def test_extract_features_empty_code(tmp_path):
    # Empty file
    code = ""
    file_name = tmp_path / "empty.py"

    features, rule_ids = analysis.extract_features_from_code(code, file_name.name)

    # Should return zeros
    assert features["pylint_total"].iloc[0] == 0
    assert features["bandit_total"].iloc[0] == 0
    assert rule_ids == []

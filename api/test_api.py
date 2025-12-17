from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_analyze_endpoint_simple_code():
    file_content = "print('Hello world')"
    response = client.post(
        "/analyze",
        files={"file": ("hello.py", file_content)}
    )
    assert response.status_code == 200
    data = response.json()
    assert "severity" in data
    assert "confidence" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)

def test_analyze_endpoint_with_bug():
    file_content = "exec('print(123)')"  
    response = client.post(
        "/analyze",
        files={"file": ("buggy.py", file_content)}
    )
    assert response.status_code == 200
    data = response.json()
    assert "severity" in data
    assert "rules_detected" in data
    assert any(r.startswith("B") for r in data["rules_detected"])

def test_analyze_endpoint_empty_file():
    file_content = "" 
    response = client.post(
        "/analyze",
        files={"file": ("empty.py", file_content)}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["features"]["pylint_total"] == 0
    assert data["features"]["bandit_total"] == 0
    assert data["rules_detected"] == []

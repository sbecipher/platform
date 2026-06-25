import pytest
from fastapi.testclient import TestClient
from scp_core.api.main import app

client = TestClient(app)

def test_daily_pms_monitor_json():
    # Because we don't have a real DB populated in the test suite, 
    # it should return the fallback mocked context data.
    response = client.get("/api/reports/pms/daily")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "markdown_content" in data
    assert "# " in data["markdown_content"] # Checking if it rendered markdown

def test_daily_pms_monitor_pdf():
    response = client.get("/api/reports/pms/daily/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF") # Magic bytes for PDF

def test_lp_diligence_brief_json():
    run_id = "test-run-123"
    response = client.get(f"/api/reports/{run_id}/markdown")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert run_id in data["markdown_content"]

def test_lp_diligence_brief_pdf():
    run_id = "test-run-123"
    response = client.get(f"/api/reports/{run_id}/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")

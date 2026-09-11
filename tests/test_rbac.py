import os
import pytest
from fastapi.testclient import TestClient
from backend.app.core.rbac import ROLE_PERMISSIONS, require_permission
from backend.app.core.audit import AUDIT_LOG_FILE, log_security_event
from backend.app.main import app

client = TestClient(app)

def test_rbac_matrix_integrity():
    assert "read:kpis" in ROLE_PERMISSIONS["Admin"]
    assert "admin:write" in ROLE_PERMISSIONS["Admin"]
    assert "admin:write" not in ROLE_PERMISSIONS["Viewer"]

def test_audit_logging():
    log_security_event("test_event", "test@insightbi.ai", "SUCCESS", {"detail": "unit_test"})
    assert os.path.exists(AUDIT_LOG_FILE)
    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        assert "test_event" in content

def test_auth_refresh_token():
    # 1. Register & Login
    reg_payload = {
        "email": "executive@insightbi.ai",
        "password": "SecurePassword123!",
        "full_name": "Chief Executive Officer",
        "role": "Executive"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_res = client.post("/api/v1/auth/login", json={
        "email": "executive@insightbi.ai",
        "password": "SecurePassword123!"
    })
    token = login_res.json()["access_token"]

    # 2. Refresh Token
    ref_res = client.post("/api/v1/auth/refresh", json={"refresh_token": token})
    assert ref_res.status_code == 200
    assert "access_token" in ref_res.json()

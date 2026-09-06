"""
Updated Production End-to-End Test Suite:
1. Health & Readiness checks
2. ML Prediction Pipeline & Feature Imputation
3. GIS GeoJSON & Heatmap endpoints
4. User Authentication & JWT RBAC (Role isolation test)
5. Field Hazard Report Submission & Status Governance Workflow
6. Protected Targeted Emergency Broadcast & Batch Alert Synchronization
"""

import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_dir)

from fastapi.testclient import TestClient
from main import app
import database

client = TestClient(app)


def test_1_health_and_ready():
    database.init_pool()
    database.init_schema()

    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    body = res.json()
    assert body["status"] == "healthy"
    assert body["ml_models"]["final_model"] is True
    print("Test 1: Health and Readiness Endpoints [PASS]")


def test_2_ml_prediction():
    payload = {
        "latitude": 27.3389,
        "longitude": 88.6065,
    }
    res = client.post("/api/v1/predictions", json=payload)
    assert res.status_code == 200, f"Prediction failed: {res.text}"
    body = res.json()
    assert "prediction_id" in body
    assert "risk_level" in body
    assert "probability" in body
    assert 0.0 <= body["probability"] <= 1.0
    assert "confidence" in body
    print(f"Test 2: ML Prediction (Prob: {body['probability']*100:.1f}%, Risk: {body['risk_level']}) [PASS]")


def test_3_gis_endpoints():
    res1 = client.get("/api/v1/gis/risk-zones")
    assert res1.status_code == 200
    geojson = res1.json()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) > 0

    res2 = client.get("/api/v1/gis/heatmap")
    assert res2.status_code == 200
    heatmap = res2.json()
    assert "points" in heatmap
    assert len(heatmap["points"]) > 0
    print(f"Test 3: GIS GeoJSON ({len(geojson['features'])} zones) & Heatmap ({len(heatmap['points'])} points) [PASS]")


def test_4_auth_and_rbac():
    # Login as default Admin
    login_data = {
        "username": "m.rithish1882007@gmail.com",
        "password": "admin123"
    }
    res = client.post("/api/v1/auth/login", data=login_data)
    assert res.status_code == 200, f"Admin login failed: {res.text}"
    token = res.json()["access_token"]
    assert len(token) > 20

    # Verify protected /auth/me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["role"] == "ADMIN"

    # Test registration privilege escalation defense: role parameter ignored, forced to CITIZEN
    reg_data = {
        "email": f"testuser_{os.urandom(3).hex()}@test.com",
        "password": "Password123!",
        "full_name": "Test Citizen",
        "role": "ADMIN"  # Malicious escalation attempt
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_data)
    assert reg_res.status_code == 200
    assert reg_res.json()["user"]["role"] == "CITIZEN", "Privilege escalation detected: role was not forced to CITIZEN"

    print("Test 4: JWT Auth & RBAC Privilege Escalation Defense [PASS]")
    return headers


def test_5_field_reporting_workflow(headers):
    # Submit report
    rep_payload = {
        "location": "NH-10 Highway Mile 24, Mangan",
        "state": "Sikkim",
        "latitude": 27.5118,
        "longitude": 88.5292,
        "hazard_type": "landslide",
        "severity": "high",
        "description": "Active ground cracks observed across highway corridor.",
        "visible_cracks": True,
        "road_blocked": True,
        "idempotency_key": f"test_rep_{os.urandom(4).hex()}"
    }
    res = client.post("/api/v1/reports", json=rep_payload, headers=headers)
    assert res.status_code == 200, f"Report submission failed: {res.text}"
    report_id = res.json()["report_id"]

    # Test idempotency (submitting same idempotency key)
    dup_res = client.post("/api/v1/reports", json=rep_payload, headers=headers)
    assert dup_res.status_code == 200
    assert dup_res.json()["report_id"] == report_id

    # Update status (Governance workflow)
    update_payload = {
        "status": "ACTION_REQUIRED",
        "admin_notes": "SDRF disaster response team dispatched to clear debris."
    }
    status_res = client.patch(f"/api/v1/reports/{report_id}/status", json=update_payload, headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["new_status"] == "ACTION_REQUIRED"
    print("Test 5: Field Reporting & Governance Status Workflow [PASS]")


def test_6_targeted_emergency_dispatch(headers):
    # Unauthenticated dispatch must fail with 401
    unauth_payload = {
        "state": "Sikkim",
        "area": "Gangtok",
        "risk_level": "CRITICAL",
        "probability": 0.95
    }
    unauth_res = client.post("/api/v1/notifications/targeted-dispatch", json=unauth_payload)
    assert unauth_res.status_code == 401, "Unauthenticated dispatch should be rejected with 401"

    # Authenticated dispatch by ADMIN
    auth_res = client.post("/api/v1/notifications/targeted-dispatch", json=unauth_payload, headers=headers)
    assert auth_res.status_code == 200, f"Targeted dispatch failed: {auth_res.text}"
    body = auth_res.json()
    assert body["success"] is True
    assert body["state"] == "Sikkim"
    print(f"Test 6: Protected Targeted Emergency Dispatch (State: {body['state']}, Area: {body['area']}) [PASS]")


if __name__ == "__main__":
    print("=" * 60)
    print("NER PLATFORM PRODUCTION TEST SUITE")
    print("=" * 60)
    test_1_health_and_ready()
    test_2_ml_prediction()
    test_3_gis_endpoints()
    admin_headers = test_4_auth_and_rbac()
    test_5_field_reporting_workflow(admin_headers)
    test_6_targeted_emergency_dispatch(admin_headers)
    print("=" * 60)
    print("ALL 6 PRODUCTION ARCHITECTURE TESTS PASSED [100% OK]")
    print("=" * 60)

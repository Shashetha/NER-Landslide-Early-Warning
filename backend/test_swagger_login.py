import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app
import database

database.init_pool()
client = TestClient(app)

# Test Swagger UI OAuth2 form submission
form_data = {
    "username": "m.rithish1882007@gmail.com",
    "password": "admin123"
}

res = client.post("/api/v1/auth/login", data=form_data)
print("HTTP Status:", res.status_code)
print("Response JSON:", res.json())

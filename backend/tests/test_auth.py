from fastapi.testclient import TestClient
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "jotester",
        "email": "jyothi@example.com",
        "password": "1234",
        "confirm_password": "1234"
    })

    print("STATUS:", response.status_code)
    print("BODY:", response.json())

    assert response.status_code == 200 or response.status_code == 400  # adjust based on existing user

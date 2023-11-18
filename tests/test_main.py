from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"message": "API is up and running all dandy and fandy!"}

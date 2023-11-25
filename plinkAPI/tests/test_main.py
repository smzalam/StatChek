from fastapi import FastAPI
from fastapi.testclient import TestClient

from plinkAPI.src.server import app
from plinkAPI.src.middleware.data_adapter import db_service as cache_funcs
from plinkAPI.src.config import constants as constants

client = TestClient(app.app)


def test_health_check():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"message": "API is up and running all dandy and fandy!"}

# def pytest_sessionfinish(session, exitstatus):
#     for directory in constants.ALL_CACHE_DIRECTORIES:
#         print(f'Deleting {directory}')
#         cache_funcs.update_cache(directory)
#         print(f'Deleted {directory}')

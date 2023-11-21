import pytest
from fastapi import status
from tests.test_main import client


@pytest.fixture(scope="session")
def test_user_auth_token():
    request = client.post(
        "users/login",
        json={
            "email": "testuseremail@gmail.com",
            "password": "testinguserpw",
        },
    )

    token = request.json()["token"]
    print(token)
    return token


@pytest.fixture()
def success_status_code():
    return status.HTTP_200_OK


@pytest.fixture()
def created_status_code():
    return status.HTTP_201_CREATED


@pytest.fixture()
def deleted_status_code():
    return status.HTTP_200_OK

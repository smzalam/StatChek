import pytest
from fastapi import status


@pytest.fixture()
def success_status_code():
    return status.HTTP_200_OK


@pytest.fixture()
def created_status_code():
    return status.HTTP_201_CREATED


@pytest.fixture()
def deleted_status_code():
    return status.HTTP_200_OK

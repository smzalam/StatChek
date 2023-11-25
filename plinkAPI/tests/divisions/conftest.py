import pytest

from plinkAPI.src.config import constants as constants
from plinkAPI.src.routers.divisions import schemas as schemas


@pytest.fixture(scope="package")
def divisions_length():
    return 4


@pytest.fixture(scope="package")
def divisions_one_data_length():
    return 1


@pytest.fixture(scope="package")
def division_ids():
    return constants.ALL_DIVISION_IDS

@pytest.fixture(scope="package")
def team_ids():
    return constants.ALL_TEAM_IDS

@pytest.fixture()
def division_ids_schema():
    return schemas.DivisionsIds

@pytest.fixture()
def division_all_schema():
    return schemas.DivisionsRequest

@pytest.fixture()
def team_all_schema():
    return schemas.TeamsRequest

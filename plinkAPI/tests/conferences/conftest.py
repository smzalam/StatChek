import pytest

from plinkAPI.src.config import constants as constants
from plinkAPI.src.routers.conferences import schemas as schemas


@pytest.fixture(scope="package")
def conferences_length():
    return 2


@pytest.fixture(scope="package")
def conferences_one_data_length():
    return 1


@pytest.fixture(scope="package")
def conference_ids():
    return constants.ALL_CONFERENCE_IDS

@pytest.fixture(scope="package")
def division_ids():
    return constants.ALL_DIVISION_IDS

@pytest.fixture(scope="package")
def team_ids():
    return constants.ALL_TEAM_IDS

@pytest.fixture()
def conference_ids_schema():
    return schemas.ConferenceIds

@pytest.fixture()
def conference_all_schema():
    return schemas.ConferencesRequest

@pytest.fixture()
def division_all_schema():
    return schemas.DivisionsRequest

@pytest.fixture()
def team_all_schema():
    return schemas.TeamsRequest

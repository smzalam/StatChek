import pytest

from tests.test_main import client
from src.app.conferences import constants as constants
from src.app.conferences import schemas as schemas


@pytest.fixture(scope="package")
def conferences_length():
    return 2


@pytest.fixture(scope="package")
def conferences_id_data_length():
    return 1


@pytest.fixture(scope="package")
def conference_ids():
    return constants.ALL_CONFERENCE_IDS


@pytest.fixture()
def conference_ids_schema():
    return schemas.ConferenceIds


@pytest.fixture()
def conference_all_schema():
    return schemas.ConferencesRequest

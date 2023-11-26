import pytest

from src.config import constants as constants
from src.routers.players import schemas as schemas


@pytest.fixture(scope="package")
def players_length():
    return 1


@pytest.fixture(scope="package")
def team_ids():
    return constants.ALL_TEAM_IDS

@pytest.fixture()
def player_data_schema():
    return schemas.PlayersRequest

@pytest.fixture()
def player_all_schema():
    return schemas.Players
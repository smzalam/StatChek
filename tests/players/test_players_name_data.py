import collections
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from tests.test_main import client


"""
/PLAYERS/NAME/:PLAYERNAME
"""


@pytest.fixture
def players_endpoint_response(
    test_user_auth_token, players_endpoint_response_arg
):
    response = client.get(
        f"/players/name/{players_endpoint_response_arg}",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


@pytest.mark.parametrize("players_endpoint_response_arg", ['Sidney Crosby', pytest.param('Test Player', marks=pytest.mark.xfail)])
def test_player_id_data_status(players_endpoint_response, success_status_code):
    assert players_endpoint_response.status_code == success_status_code


@pytest.mark.parametrize("players_endpoint_response_arg", ['Sidney Crosby', pytest.param('Test Player', marks=pytest.mark.xfail)])
def test_player_all_response_body_attrs(
    players_endpoint_response, player_all_schema, player_data_schema
):
    players = players_endpoint_response.json()
    assert player_all_schema.model_validate_json(json.dumps(players))
    for player in players["data"]:
        assert player_data_schema.model_validate_json(json.dumps(player))

@pytest.mark.parametrize("players_endpoint_response_arg", ['Sidney Crosby', pytest.param('Test Player', marks=pytest.mark.xfail)])
def test_player_all_response_body_len(
    players_endpoint_response
):
    players = players_endpoint_response.json()
    assert type(players["player"]) == str

@pytest.mark.parametrize("players_endpoint_response_arg", ['Sidney Crosby', pytest.param('Test Player', marks=pytest.mark.xfail)])
def test_player_all_player_attr(players_endpoint_response, team_ids):
    players = players_endpoint_response.json()
    for player in players["data"]:
        assert player["team_id"] in team_ids

@pytest.mark.parametrize("players_endpoint_response_arg", [pytest.param('Test Player', marks=pytest.mark.xfail)])
def test_player_bad_request_error(players_endpoint_response):
    details = players_endpoint_response.json()
    assert details['message'] == 'Player Name does not exist'
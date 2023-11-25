import collections
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from plinkAPI.tests.test_main import client


"""
/CONFERENCES/:conferenceID/all
"""


@pytest.fixture
def conferences_endpoint_response(
    test_user_auth_token, conferences_endpoint_response_arg
):
    response = client.get(
        f"/conferences/{conferences_endpoint_response_arg}/all",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_id_data_status(conferences_endpoint_response, success_status_code):
    assert conferences_endpoint_response.status_code == success_status_code


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_body_len(
    conferences_endpoint_response, conferences_one_data_length
):
    conferences = conferences_endpoint_response.json()
    assert len(conferences["conferences"]) == conferences_one_data_length

@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_division_body_len(
    conferences_endpoint_response, conferences_one_data_length
):
    conferences = conferences_endpoint_response.json()
    divisions = conferences["conferences"][0]['divisions']
    assert len(divisions) == 2

@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_teams_body_len(
    conferences_endpoint_response, conferences_one_data_length
):
    conferences = conferences_endpoint_response.json()
    teams = conferences["conferences"][0]['teams']
    assert len(teams) >= 16


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_body_validation(
    conferences_endpoint_response, conference_all_schema
):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        assert conference_all_schema.model_validate_json(json.dumps(conference))

@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_division_body_validation(
    conferences_endpoint_response, division_all_schema
):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        for division in conference['divisions']:
            assert division_all_schema.model_validate_json(json.dumps(division))

@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_team_body_validation(
    conferences_endpoint_response, team_all_schema
):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        for team in conference['teams']:
            assert team_all_schema.model_validate_json(json.dumps(team))


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_ids_validation(conferences_endpoint_response, conference_ids):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        assert conference['conference_id'] in conference_ids
        if conference["conference_id"] == 6:
            assert conference["name"] == "Eastern"
        if conference["conference_id"] == 5:
            assert conference["name"] == "Western"

@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_division_ids_validation(conferences_endpoint_response, division_ids):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        for division in conference['divisions']:
            assert division['division_id'] in division_ids

@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_response_division_ids_validation(conferences_endpoint_response, team_ids):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        for team in conference['teams']:
            assert team['team_id'] in team_ids
import collections
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from tests.test_main import client


"""
/CONFERENCES/:conferenceID
"""


@pytest.fixture
def conferences_endpoint_response(
    test_user_auth_token, conferences_endpoint_response_arg
):
    response = client.get(
        f"/conferences/{conferences_endpoint_response_arg}",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_id_data_status(conferences_endpoint_response, success_status_code):
    assert conferences_endpoint_response.status_code == success_status_code


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_all_response_body_len(
    conferences_endpoint_response, conferences_one_data_length
):
    conferences = conferences_endpoint_response.json()
    assert len(conferences["conferences"]) == conferences_one_data_length


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_all_response_body_attrs(
    conferences_endpoint_response, conference_all_schema
):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        assert conference_all_schema.model_validate_json(json.dumps(conference))


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_all_division_attr(conferences_endpoint_response):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        assert conference["divisions"] == "Not Requested"
        assert conference["teams"] == "Not Requested"


@pytest.mark.parametrize("conferences_endpoint_response_arg", [5, 6])
def test_conference_all_correct_matching_id_name(conferences_endpoint_response):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        if conference["conference_id"] == 6:
            assert conference["name"] == "Eastern"
        if conference["conference_id"] == 5:
            assert conference["name"] == "Western"

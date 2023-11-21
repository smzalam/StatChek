import collections
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from tests.test_main import client


"""
/CONFERENCES/IDS
"""


@pytest.fixture(scope="module")
def conferences_endpoint_response(test_user_auth_token):
    response = client.get(
        "/conferences",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


def test_conference_all_status(conferences_endpoint_response, success_status_code):
    assert conferences_endpoint_response.status_code == success_status_code


def test_conference_all_response_body_len(
    conferences_endpoint_response, conferences_length
):
    conferences = conferences_endpoint_response.json()
    assert len(conferences["conferences"]) == conferences_length


def test_conference_all_response_body_attrs(
    conferences_endpoint_response, conference_all_schema
):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        assert conference_all_schema.model_validate_json(json.dumps(conference))


def test_conference_all_ids(conferences_endpoint_response, conference_ids):
    conferences = conferences_endpoint_response.json()
    conference_response_ids = [
        conferences["conferences"][i]["conference_id"]
        for i in range(0, len(conferences["conferences"]))
    ]
    assert collections.Counter(conference_response_ids) == collections.Counter(
        conference_ids
    )


def test_conference_all_division_attr(conferences_endpoint_response):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        assert conference["divisions"] == "Not Requested"
        assert conference["teams"] == "Not Requested"


def test_conference_all_correct_matching_id_name(conferences_endpoint_response):
    conferences = conferences_endpoint_response.json()
    for conference in conferences["conferences"]:
        if conference["conference_id"] == 6:
            assert conference["name"] == "Eastern"
        if conference["conference_id"] == 5:
            assert conference["name"] == "Western"

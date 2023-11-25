import json
import collections
from pprint import pprint

import pytest
from pydantic import ValidationError

from plinkAPI.tests.test_main import client


"""
/DIVISIONS
"""


@pytest.fixture(scope="module")
def divisions_endpoint_response(test_user_auth_token):
    response = client.get(
        "/divisions",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


def test_division_all_status(divisions_endpoint_response, success_status_code):
    assert divisions_endpoint_response.status_code == success_status_code


def test_division_all_response_body_len(
    divisions_endpoint_response, divisions_length
):
    divisions = divisions_endpoint_response.json()
    assert len(divisions["divisions"]) == divisions_length


def test_division_all_response_body_attrs(
    divisions_endpoint_response, division_all_schema
):
    divisions = divisions_endpoint_response.json()
    for division in divisions["divisions"]:
        assert division_all_schema.model_validate_json(json.dumps(division))


def test_division_all_ids(divisions_endpoint_response, division_ids):
    divisions = divisions_endpoint_response.json()
    division_response_ids = [
        divisions["divisions"][i]["division_id"]
        for i in range(0, len(divisions["divisions"]))
    ]
    assert collections.Counter(division_response_ids) == collections.Counter(
        division_ids
    )


def test_division_all_division_attr(divisions_endpoint_response):
    divisions = divisions_endpoint_response.json()
    for division in divisions["divisions"]:
        assert division["teams"] == "Not Requested"


def test_division_all_correct_matching_id_name(divisions_endpoint_response):
    divisions = divisions_endpoint_response.json()
    for division in divisions["divisions"]:
        if division["division_id"] == 17:
            assert division["name"] == "Atlantic"
        if division["division_id"] == 16:
            assert division["name"] == "Central"
        if division["division_id"] == 18:
            assert division["name"] == "Metropolitan"
        if division["division_id"] == 15:
            assert division["name"] == "Pacific"
        

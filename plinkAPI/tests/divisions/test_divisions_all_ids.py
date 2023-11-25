import collections
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from plinkAPI.tests.test_main import client



"""
/DIVISIONS/IDS
"""


@pytest.fixture(scope="module")
def divisions_endpoint_response(test_user_auth_token):
    response = client.get(
        "/divisions/ids",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


def test_division_ids_status(divisions_endpoint_response, success_status_code):
    assert divisions_endpoint_response.status_code == success_status_code


def test_division_ids_response_body_len(
    divisions_endpoint_response, divisions_length
):
    divisions = divisions_endpoint_response.json()
    assert len(divisions["division_ids"]) == divisions_length


def test_division_ids_response_body_attrs(
    divisions_endpoint_response, division_ids_schema
):
    divisions = divisions_endpoint_response.json()
    for division in divisions["division_ids"]:
        assert division_ids_schema.model_validate_json(json.dumps(division))


def test_division_ids_validaiton(divisions_endpoint_response, division_ids):
    divisions = divisions_endpoint_response.json()
    division_response_ids = [
        divisions["division_ids"][i]["division_id"]
        for i in range(0, len(divisions["division_ids"]))
    ]
    assert collections.Counter(division_response_ids) == collections.Counter(
        division_ids
    )

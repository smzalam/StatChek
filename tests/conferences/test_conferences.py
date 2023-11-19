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
def conferences_endpoint_response():
    response = client.get("/conferences/ids")
    return response


def test_conference_ids_status(conferences_endpoint_response, success_status_code):
    assert conferences_endpoint_response.status_code == success_status_code


def test_conference_ids_response_body_len(
    conferences_endpoint_response, conferences_length
):
    conferences = conferences_endpoint_response.json()
    assert len(conferences["conference_ids"]) == conferences_length


def test_conference_ids_response_body_attrs(
    conferences_endpoint_response, conference_ids_schema
):
    conferences = conferences_endpoint_response.json()
    validation_error_count = 0
    for conference in conferences["conference_ids"]:
        assert conference_ids_schema.model_validate_json(json.dumps(conference))


def test_conference_ids_all_ids(conferences_endpoint_response, conference_ids):
    conferences = conferences_endpoint_response.json()
    conference_response_ids = [
        conferences["conference_ids"][i]["conference_id"]
        for i in range(0, len(conferences["conference_ids"]))
    ]
    assert collections.Counter(conference_response_ids) == collections.Counter(
        conference_ids
    )

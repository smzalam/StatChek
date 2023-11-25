import collections
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from plinkAPI.tests.test_main import client


"""
/DIVISIONS/:DIVISIONID
"""


@pytest.fixture
def divisions_endpoint_response(
    test_user_auth_token, divisions_endpoint_response_arg
):
    response = client.get(
        f"/divisions/{divisions_endpoint_response_arg}",
        headers={"Authorization": f"Bearer {test_user_auth_token}"},
    )
    return response


@pytest.mark.parametrize("divisions_endpoint_response_arg", [15, 16, 17, 18, pytest.param(9, marks=pytest.mark.xfail)])
def test_division_id_data_status(divisions_endpoint_response, success_status_code):
    assert divisions_endpoint_response.status_code == success_status_code


@pytest.mark.parametrize("divisions_endpoint_response_arg", [15, 16, 17, 18, pytest.param(9, marks=pytest.mark.xfail)])
def test_division_all_response_body_len(
    divisions_endpoint_response, divisions_one_data_length
):
    divisions = divisions_endpoint_response.json()
    assert len(divisions["divisions"]) == divisions_one_data_length


@pytest.mark.parametrize("divisions_endpoint_response_arg", [15, 16, 17, 18, pytest.param(9, marks=pytest.mark.xfail)])
def test_division_all_response_body_attrs(
    divisions_endpoint_response, division_all_schema
):
    divisions = divisions_endpoint_response.json()
    for division in divisions["divisions"]:
        assert division_all_schema.model_validate_json(json.dumps(division))


@pytest.mark.parametrize("divisions_endpoint_response_arg", [15, 16, 17, 18, pytest.param(9, marks=pytest.mark.xfail)])
def test_division_all_division_attr(divisions_endpoint_response):
    divisions = divisions_endpoint_response.json()
    for division in divisions["divisions"]:
        assert division["teams"] == "Not Requested"

@pytest.mark.parametrize("divisions_endpoint_response_arg", [15, 16, 17, 18, pytest.param(9, marks=pytest.mark.xfail)])
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

@pytest.mark.parametrize("divisions_endpoint_response_arg", [pytest.param(9, marks=pytest.mark.xfail)])
def test_division_bad_request_error(divisions_endpoint_response):
    details = divisions_endpoint_response.json()
    assert details['message'] == 'Division ID does not exist'
from uuid import uuid4

import jsonschema
import pytest

from api import schemas
from api.booker_client import booking_payload

FORMATS = jsonschema.FormatChecker()


def test_create_returns_the_booking_matching_the_schema(booker, token):
    payload = booking_payload()
    response = booker.create(payload)
    assert response.status_code == 200
    body = response.json()
    jsonschema.validate(body, schemas.CREATED, format_checker=FORMATS)
    assert body["booking"] == payload
    booker.delete(body["bookingid"], token)


def test_get_returns_what_was_created(booker, booking):
    booking_id, payload = booking
    response = booker.get(booking_id)
    assert response.status_code == 200
    jsonschema.validate(response.json(), schemas.BOOKING, format_checker=FORMATS)
    assert response.json() == payload


def test_update_without_a_token_is_forbidden(booker, booking):
    booking_id, payload = booking
    response = booker.update(booking_id, payload | {"firstname": "Intruder"})
    assert response.status_code == 403
    assert booker.get(booking_id).json()["firstname"] == payload["firstname"]


def test_update_with_a_token_replaces_the_booking(booker, booking, token):
    booking_id, payload = booking
    changed = payload | {"firstname": "Bia", "totalprice": 200, "depositpaid": False}
    response = booker.update(booking_id, changed, token)
    assert response.status_code == 200
    assert response.json() == changed
    assert booker.get(booking_id).json() == changed


def test_partial_update_changes_only_the_given_field(booker, booking, token):
    booking_id, payload = booking
    response = booker.patch(booking_id, {"additionalneeds": "Late checkout"}, token)
    assert response.status_code == 200
    assert response.json() == payload | {"additionalneeds": "Late checkout"}


def test_deleted_booking_is_no_longer_found(booker, token):
    booking_id = booker.create(booking_payload()).json()["bookingid"]
    booker.delete(booking_id, token)
    assert booker.get(booking_id).status_code == 404


def test_filter_by_name_finds_the_booking(booker, token):
    payload = booking_payload(lastname=f"QA-{uuid4().hex[:8]}")
    booking_id = booker.create(payload).json()["bookingid"]
    found = booker.find(firstname=payload["firstname"], lastname=payload["lastname"])
    assert found.status_code == 200
    assert {"bookingid": booking_id} in found.json()
    booker.delete(booking_id, token)


@pytest.mark.xfail(reason="BUG-010: DELETE answers 201 Created instead of 200 or 204")
def test_delete_answers_with_a_success_status(booker, token):
    booking_id = booker.create(booking_payload()).json()["bookingid"]
    assert booker.delete(booking_id, token).status_code in (200, 204)


@pytest.mark.xfail(reason="BUG-011: a booking without firstname crashes the server (500) instead of 400")
def test_missing_required_field_is_a_client_error(booker):
    payload = booking_payload()
    del payload["firstname"]
    assert booker.create(payload).status_code == 400


@pytest.mark.xfail(reason="BUG-012: check-out before check-in and a negative price are accepted")
def test_impossible_booking_is_rejected(booker, token):
    payload = booking_payload(totalprice=-5, bookingdates={"checkin": "2026-11-05", "checkout": "2026-11-01"})
    response = booker.create(payload)
    if response.ok:
        booker.delete(response.json()["bookingid"], token)
    assert response.status_code == 400

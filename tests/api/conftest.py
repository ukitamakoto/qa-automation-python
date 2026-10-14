import pytest
import requests

from api.booker_client import BookerClient, booking_payload


@pytest.fixture(scope="session")
def booker() -> BookerClient:
    client = BookerClient()
    try:
        alive = client.ping().ok
    except requests.RequestException:
        alive = False
    if not alive:
        pytest.fail(
            f"Restful-Booker is unreachable at {client.base_url}; the target is down, not the tests.",
            pytrace=False,
        )
    return client


@pytest.fixture(scope="session")
def token(booker) -> str:
    return booker.token()


@pytest.fixture
def booking(booker, token):
    """A fresh booking for one test, deleted afterwards (the API also resets every 10 minutes)."""
    payload = booking_payload()
    response = booker.create(payload)
    assert response.status_code == 200, response.text
    booking_id = response.json()["bookingid"]
    yield booking_id, payload
    booker.delete(booking_id, token)

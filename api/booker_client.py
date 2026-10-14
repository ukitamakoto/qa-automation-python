"""Thin Restful-Booker client. Returns raw responses so tests assert on status codes."""

import requests

import config


def booking_payload(**overrides) -> dict:
    booking = {
        "firstname": "Ana",
        "lastname": "Silva",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": "Breakfast",
    }
    return booking | overrides


class BookerClient:
    def __init__(self, base_url: str = config.BOOKER_URL, timeout: float = 15):
        self.base_url = base_url
        self.timeout = timeout
        self.http = requests.Session()
        self.http.headers.update({"Accept": "application/json"})

    def _call(self, method: str, path: str, token: str | None = None, **kwargs) -> requests.Response:
        cookies = {"token": token} if token else None
        return self.http.request(
            method, self.base_url + path, cookies=cookies, timeout=self.timeout, **kwargs
        )

    def ping(self):
        return self._call("GET", "/ping")

    def auth(self, username: str, password: str):
        return self._call("POST", "/auth", json={"username": username, "password": password})

    def token(self) -> str:
        return self.auth(**config.BOOKER_ADMIN).json()["token"]

    def create(self, booking: dict):
        return self._call("POST", "/booking", json=booking)

    def get(self, booking_id: int):
        return self._call("GET", f"/booking/{booking_id}")

    def find(self, **filters):
        return self._call("GET", "/booking", params=filters)

    def update(self, booking_id: int, booking: dict, token: str | None = None):
        return self._call("PUT", f"/booking/{booking_id}", token, json=booking)

    def patch(self, booking_id: int, fields: dict, token: str | None = None):
        return self._call("PATCH", f"/booking/{booking_id}", token, json=fields)

    def delete(self, booking_id: int, token: str | None = None):
        return self._call("DELETE", f"/booking/{booking_id}", token)

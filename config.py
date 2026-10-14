"""Targets and public demo credentials. Override the URLs with environment variables."""

import os

SAUCEDEMO_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com").rstrip("/")
BOOKER_URL = os.getenv("BOOKER_URL", "https://restful-booker.herokuapp.com").rstrip("/")

# Both are published by the targets themselves (SauceDemo login page, Restful-Booker docs).
SAUCE_PASSWORD = "secret_sauce"
BOOKER_ADMIN = {"username": "admin", "password": "password123"}

import pytest

import config


def test_valid_credentials_return_a_token(booker):
    response = booker.auth(**config.BOOKER_ADMIN)
    assert response.status_code == 200
    token = response.json().get("token")
    assert isinstance(token, str) and token


@pytest.mark.xfail(reason="BUG-009: wrong credentials return 200 with a 'reason' body instead of 401")
def test_wrong_credentials_return_401_without_a_token(booker):
    response = booker.auth(config.BOOKER_ADMIN["username"], "wrong-password")
    assert "token" not in response.json()
    assert response.status_code == 401

import pytest

from data.constants import (
    AUTH_CLIENT_USER_LOGIN,
    AUTH_CLIENT_USER_PASSWORD,
)


@pytest.fixture(scope="function")
def restore_session_after_test(
        auth_account_helper
):
    yield
    auth_account_helper.auth_client(login=AUTH_CLIENT_USER_LOGIN, password=AUTH_CLIENT_USER_PASSWORD)


def test_delete_v1_account_login(
        auth_account_helper,
        restore_session_after_test
):
    response = auth_account_helper.logout_user()
    assert response.status_code == 204, "Логаут пользователя не был осуществлен."

import pytest
from vyper import v


@pytest.fixture(scope="function")
def restore_session_after_test(
        auth_account_helper
):
    yield
    auth_account_helper.auth_client(login=v.get('user.login'), password=v.get('user.password'))


def test_delete_v1_account_login(
        auth_account_helper,
        restore_session_after_test
):
    response = auth_account_helper.logout_user()
    assert response.status_code == 204, "Логаут пользователя не был осуществлен."

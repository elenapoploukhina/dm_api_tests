import pytest


@pytest.fixture(scope="function", autouse=True)
def restore_session_after_test(
        auth_account_helper
):
    yield
    auth_account_helper.auth_client(login="lenaivanova_1", password="123456789")


def test_delete_v1_account_login(
        auth_account_helper
):
    response = auth_account_helper.logout_user()
    assert response.status_code == 204, "Логаут пользователя не был осуществлен."

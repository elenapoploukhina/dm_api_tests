import allure
import pytest
from vyper import v


@allure.suite("Тесты для метода c")
@allure.sub_suite("Логаут текущего авторизованного пользователя")
class TestDeleteV1Account:

    @pytest.fixture(scope="function")
    def restore_session_after_test(
            self,
            auth_account_helper
    ):
        yield
        auth_account_helper.auth_client(login=v.get('user.login'), password=v.get('user.password'))

    @allure.title("Успешный логаут текущего пользователя с активной сессией")
    def test_delete_v1_account_login(
            self,
            auth_account_helper,
            restore_session_after_test
    ):
        response = auth_account_helper.logout_user()
        assert response.status_code == 204, "Логаут пользователя не был осуществлен."

import allure
import pytest
from vyper import v


@allure.suite("Тесты для метода DELETE v1/account/login/all")
@allure.sub_suite("Логаут пользователя со всех устройств")
class TestDeleteV1AccountAll:

    @pytest.fixture(scope="function")
    def restore_session_after_test(
            self,
            auth_account_helper
    ):
        yield
        auth_account_helper.auth_client(login=v.get('user.login'), password=v.get('user.password'))

    @allure.title("Успешный логаут пользователя со всех устройств")
    def test_delete_v1_account_login_all(
            self,
            auth_account_helper,
            restore_session_after_test
    ):
        response = auth_account_helper.logout_user_from_all_devices()
        assert response.status_code == 204, "Логаут пользователя со всех устройств не был осуществлен."

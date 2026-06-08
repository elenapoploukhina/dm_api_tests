import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты для метода GET v1/account")
@allure.sub_suite("Получение информации о пользователе")
class TestGetV1Account:

    @allure.title("Успешное получение информации об авторизованном пользователе")
    def test_get_v1_account_auth(
            self,
            auth_account_helper
    ):
        response = auth_account_helper.get_user(validate_response=True)
        GetV1Account.check_response_values(response)

    @allure.title("Ошибка при получении информации о неавторизованном пользователе")
    def test_get_v1_account_no_auth(
            self,
            account_helper
    ):
        with check_status_code_http(401, "User must be authenticated"):
            account_helper.get_user(validate_response=False)

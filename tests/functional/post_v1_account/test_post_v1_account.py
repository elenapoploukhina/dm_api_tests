import allure
import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account

@allure.suite("Тесты для метода POST v1/account")
@allure.sub_suite("Регистрация нового пользователя")
class TestPostV1Account:

    @allure.title("Успешная регистрация нового пользователя")
    def test_post_v1_account(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)


    @allure.title("Регистрация нового пользователя c невалидными учетными данными")
    @pytest.mark.parametrize(
        'login, email, password, expected_status_code, error_message', [
            ('lenaivanova_31_05_2026_20', 'lenaivanova_31_05_2026_20@mail.ru', '63515', 400, 'Validation failed'),
            ('lenaivanova_31_05_2026_21', 'lenamail.ru', '123456789', 400, 'Validation failed'),
            ('l', 'lenaivanova_31_05_2026_22@mail.ru', '123456789', 400, 'Validation failed')
        ]
    )
    def test_post_v1_account_failed_validation(
            self,
            account_helper,
            login,
            email,
            password,
            expected_status_code,
            error_message
    ):
        with check_status_code_http(expected_status_code, error_message):
            account_helper.register_new_user(login=login, password=password, email=email)

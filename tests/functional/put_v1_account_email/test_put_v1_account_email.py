import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты для метода PUT v1/account/email")
@allure.sub_suite("Изменение email зарегистрированного пользователя")
class TestPutV1AccountEmail:

    @allure.title("Успешное изменение email зарегистрированного пользователя")
    def test_put_v1_account_email(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        assert response.status_code == 200, "Пользователь не смог авторизоваться."
        new_email = f'{login}_new@mail.ru'
        account_helper.change_email(login=login, password=password, email=new_email)
        with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
            account_helper.user_login(login=login, password=password)
        account_helper.confirm_email_change(login=login)
        response = account_helper.user_login(login=login, password=password)
        assert response.status_code == 200, "Пользователь не смог авторизоваться."

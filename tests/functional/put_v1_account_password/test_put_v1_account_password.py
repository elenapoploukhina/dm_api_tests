import allure


@allure.suite("Тесты для метода PUT v1/account/password")
@allure.sub_suite("Изменение пароля зарегистрированного пользователя")
class TestPutV1AccountPassword:

    @allure.title("Успешное изменение пароля зарегистрированного пользователя")
    def test_put_v1_account_password(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        new_password = "0987654321"
        account_helper.change_password(login=login, email=email, old_password=password, new_password=new_password)
        account_helper.user_login(login=login, password=new_password)

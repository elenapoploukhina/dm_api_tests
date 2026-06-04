import allure


@allure.suite("Тесты для метода PUT v1/account/token")
@allure.sub_suite("Активация зарегистрированного пользователя")
class TestPutV1AccountToken:

    @allure.title("Успешная активация нового зарегистрированного пользователя")
    def test_put_v1_account_token(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=False)
        assert response.status_code == 200, "Пользователь не смог авторизоваться."

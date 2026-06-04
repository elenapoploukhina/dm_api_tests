import allure


@allure.suite("Тесты для метода POST v1/account/login")
@allure.sub_suite("Авторизация пользователя")
class TestPostV1AccountLogin:

    @allure.title("Успешный логин нового пользователя")
    def test_post_v1_account_login(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password, validate_response=True)
        # assert response.status_code == 200, "Пользователь не смог авторизоваться."
        # assert response.headers.get("x-dm-auth-token"), "Токен для пользователя не был получен"

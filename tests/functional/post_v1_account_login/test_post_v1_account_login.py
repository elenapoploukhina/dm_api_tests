def test_post_v1_account_login(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password, validate_response=True)
    # Тут пока непонятно, как проверить одновременно и модель ответа, и статус код, и хедер
    # assert response.status_code == 200, "Пользователь не смог авторизоваться."
    # assert response.headers.get("x-dm-auth-token"), "Токен для пользователя не был получен"

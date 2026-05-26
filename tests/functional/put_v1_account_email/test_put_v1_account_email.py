def test_put_v1_account_email(
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
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, "Попытка входа должна быть заблокирована."
    account_helper.confirm_email_change(login=login)
    account_helper.user_login(login=login, password=password)

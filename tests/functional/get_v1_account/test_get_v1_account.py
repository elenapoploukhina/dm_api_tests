def test_get_v1_account_auth(
        auth_account_helper
):
    auth_account_helper.get_user(validate_response=True)
    # Пока убрали assert, потому что выполняем только валидацию модели ответа
    # assert response.status_code == 200, "Пользователь не был получен."


def test_get_v1_account_no_auth(
        account_helper
):
    response = account_helper.get_user(validate_response=False)
    assert response.status_code == 401, "Статус авторизации пользователя неожидаемый."

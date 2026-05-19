from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True
            # sort_keys=True
        )
    ]
)


def test_put_v1_account_email():
    mail_hog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025")
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mail_hog_configuration)

    # Зарегистрировать пользователя
    login = 'lenaivanova_39'
    email = f'{login}@mail.ru'
    password = '123456789'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан. {response.json()=}"

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены."

    # Получить активационный токен из письма
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен."

    # Активировать пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован."

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не смог авторизоваться."

    # Изменить email
    new_email = f'{login}_new@mail.ru'
    json_data = {
        'login': login,
        'password': password,
        'email': new_email,
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, "Не получилось изменить пароль пользователя."

    # Авторизоваться с ошибкой 403
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, "Попытка входа должна быть заблокирована."

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены."

    # Получить активационный токен из письма
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен."

    # Активировать пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован."

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не смог авторизоваться."


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()["items"]:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            break
    return token

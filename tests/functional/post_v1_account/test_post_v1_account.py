from json import loads

import structlog

from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.api_mailhog import MailHog
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True
            # sort_keys=True
        )
    ]
)


def test_post_v1_account():
    mail_hog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025")
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_log=False)

    account = DMApiAccount(dm_api_configuration)
    mailhog = MailHog(mail_hog_configuration)

    # Зарегистрировать пользователя
    login = 'lenaivanova_40'
    email = f'{login}@mail.ru'
    password = '123456789'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не был создан. {response.json()=}"

    # Получить письма из почтового сервера
    response = mailhog.mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены."

    # Получить активационный токен из письма
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Токен для пользователя {login} не был получен."

    # Активировать пользователя
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован."

    # Авторизоваться (проверка, что пользователь активирован)
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account.login_api.post_v1_account_login(json_data=json_data)
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

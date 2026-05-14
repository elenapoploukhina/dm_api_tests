import requests
import json


def test_post_v1_account():
    """Регистрация и активация пользователя"""
    # Зарегистрировать пользователя
    login = 'lenaivanova_1'
    email = f'{login}@mail.ru'
    password = '123456789'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получить письма из почтового сервера
    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # Получить активационный токен из письма
    ...

    # Активировать пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://185.185.143.231:5051/v1/account/af8a660a-ff23-487f-8cb6-e6f6cf313002',
                            headers=headers)
    print(response.status_code)
    print(response.text)

    # Авторизоваться (проверка, что пользователь активирован)
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)

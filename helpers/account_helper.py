import time
from enum import (
    Enum,
    auto,
)
from json import loads

from requests import Response
from retrying import retry

from services.api_mailhog import MailHog
from services.dm_api_account import DMApiAccount


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retryer(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            token = function(*args, **kwargs)
            count += 1
            print(f'Попытка получения токена номер {count}')
            if token:
                return token
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена.")
            time.sleep(1)

    return wrapper


class EmailType(Enum):
    USER_REGISTRATION = auto()
    PASSWORD_RESET = auto()
    EMAIL_CHANGE = auto()


class AccountHelper:
    def __init__(
            self,
            dm_api_account: DMApiAccount,
            mailhog: MailHog
    ):
        self.dm_api_account = dm_api_account
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)
        token_header = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_api_account.account_api.set_headers(token_header)
        self.dm_api_account.login_api.set_headers(token_header)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ) -> Response:
        """
        Зарегистрировать и активировать нового пользователя
        :param login:
        :param password:
        :param email:
        :return:
        """
        # Зарегистрировать пользователя
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_api_account.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не был создан. {response.json()=}"

        # Получить активационный токен из письма
        token = self._get_token_from_email(login=login, email_type=EmailType.USER_REGISTRATION)
        assert token is not None, f"Токен для пользователя {login} не был получен."

        # Активировать пользователя
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован."

        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ) -> Response:
        """
        Авторизоваться в системе
        :param login:
        :param password:
        :param remember_me:
        :return:
        """
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не смог авторизоваться."
        return response

    def user_login_forbidden(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ) -> Response:
        """
        Авторизоваться в системе, когда доступ запрещен.
        :param login:
        :param password:
        :param remember_me:
        :return:
        """
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, "Попытка входа должна быть заблокирована."
        return response

    def change_email(
            self,
            login: str,
            password: str,
            email: str
    ) -> Response:
        """
        Изменить email пользователя
        :param login:
        :param password:
        :param email:
        :return:
        """
        # Изменить email
        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }
        response = self.dm_api_account.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Не получилось изменить пароль пользователя."

        return response

    def confirm_email_change(
            self,
            login: str
    ) -> Response:
        """
        Подтвердить смену email пользователя при помощи активационного токена
        :param login:
        :return:
        """
        # Получить активационный токен из письма
        token = self._get_token_from_email(login=login, email_type=EmailType.EMAIL_CHANGE)
        assert token is not None, f"Токен для пользователя {login} не был получен."

        # Активировать пользователя с новым email
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован после смены email."

        return response

    def get_user(
            self
    ):
        """
        Получить текущего авторизованного пользователя
        :return:
        """
        response = self.dm_api_account.account_api.get_v1_account()
        return response

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ) -> Response:
        """
        Сбросить пароль для пользователя
        :param login: логин пользователя
        :param email: почта пользователя
        :param old_password: старый пароль
        :param new_password: новый пароль
        :return:
        """
        # Получить токен авторизации и сформировать header авторизации
        response = self.user_login(login=login, password=old_password)
        token_header = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }

        # Сбросить пароль
        reset_password_json_data = {
            "login": login,
            "email": email
        }
        response = self.dm_api_account.account_api.post_v1_account_password(json_data=reset_password_json_data)
        assert response.status_code == 200, "Не получилось сбросить пароль."

        # Получить токен для сброса пароля из подтверждающего письма
        token = self._get_token_from_email(login=login, email_type=EmailType.PASSWORD_RESET)
        assert token is not None, f"Токен для пользователя {login} не был получен."

        # Поменять пароль на новый
        change_password_json_data = {
            "login": login,
            "token": token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        response = self.dm_api_account.account_api.put_v1_account_password(
            json_data=change_password_json_data, headers=token_header
        )
        assert response.status_code == 200, "Не получилось изменить пароль."

        return response

    @retry(retry_on_result=retry_if_result_none, stop_max_attempt_number=5, wait_fixed=1000)
    def _get_token_from_email(
            self,
            login: str,
            email_type: EmailType
    ) -> str:
        """
        Получить токен для пользователя по его логину из списка писем
        :param login: логин пользователя
        :param email_type: тип письма для извлечения токена
        :return: активационный токен
        """
        token = None
        # Получить письма из почтового сервера
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        match email_type:
            case EmailType.USER_REGISTRATION | EmailType.EMAIL_CHANGE:
                link_key = 'ConfirmationLinkUrl'
            case EmailType.PASSWORD_RESET:
                link_key = 'ConfirmationLinkUri'
            case _:
                raise ValueError('Неподдерживаемый тип письма.')

        for item in response.json()["items"]:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login != login:
                continue
            link_url = user_data.get(link_key)
            if link_url:
                token = link_url.split('/')[-1]
                break
        return token

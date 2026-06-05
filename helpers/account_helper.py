import time
from enum import (
    Enum,
    auto,
)
from json import loads

import allure
from retrying import retry

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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
        """
        Авторизовать классы-клиенты
        :param login:
        :param password:
        :return:
        """
        response = self.user_login(login=login, password=password, validate_response=False)
        assert response.headers.get("x-dm-auth-token"), "Токен для пользователя не был получен"
        assert response.status_code == 200, "Пользователь не смог авторизоваться."
        token_header = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_api_account.account_api.set_headers(token_header)
        self.dm_api_account.login_api.set_headers(token_header)

    @allure.step("Зарегистрировать и активировать пользователя")
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        """
        Зарегистрировать и активировать нового пользователя
        :param login:
        :param password:
        :param email:
        :return:
        """
        # Зарегистрировать пользователя
        registration = Registration(login=login, password=password, email=email)
        response = self.dm_api_account.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан. {response.json()=}"

        start_time = time.time()
        # Получить активационный токен из письма
        token = self._get_token_from_email(login=login, email_type=EmailType.USER_REGISTRATION)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен."

        # Активировать пользователя
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)

        return response

    @allure.step("Авторизоваться в системе")
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = True,
            validate_headers: bool = False
    ):
        """
        Авторизоваться в системе
        :param login:
        :param password:
        :param remember_me:
        :param validate_response:
        :param validate_headers:
        :return:
        """
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)
        response = self.dm_api_account.login_api.post_v1_account_login(
            login_credentials=login_credentials, validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        return response

    @allure.step("Изменить email пользователя")
    def change_email(
            self,
            login: str,
            password: str,
            email: str
    ):
        """
        Изменить email пользователя
        :param login:
        :param password:
        :param email:
        :return:
        """
        change_email = ChangeEmail(login=login, password=password, email=email)
        response = self.dm_api_account.account_api.put_v1_account_email(change_email=change_email)
        return response

    @allure.step("Подтвердить изменение email пользователя")
    def confirm_email_change(
            self,
            login: str
    ):
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
        return response

    @allure.step("Получить информацию о пользователе")
    def get_user(
            self,
            validate_response: bool = True
    ):
        """
        Получить информацию о пользователе
        :param validate_response:
        :return:
        """
        response = self.dm_api_account.account_api.get_v1_account(validate_response=validate_response)
        return response

    @allure.step("Изменить пароль пользователя")
    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        """
        Изменить пароль для пользователя
        :param login: логин пользователя
        :param email: почта пользователя
        :param old_password: старый пароль
        :param new_password: новый пароль
        :return:
        """
        # Получить токен авторизации и сформировать header авторизации
        response = self.user_login(login=login, password=old_password, validate_response=False)
        assert response.status_code == 200, "Пользователь не смог авторизоваться."
        assert response.headers.get("x-dm-auth-token"), "Токен для пользователя не был получен"
        token_header = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }

        # Сбросить пароль
        reset_password = ResetPassword(login=login, email=email)
        self.dm_api_account.account_api.post_v1_account_password(reset_password=reset_password)

        # Получить токен для сброса пароля из подтверждающего письма
        token = self._get_token_from_email(login=login, email_type=EmailType.PASSWORD_RESET)
        assert token is not None, f"Токен для пользователя {login} не был получен."

        # Поменять пароль на новый
        change_password = ChangePassword(login=login, token=token, old_password=old_password, new_password=new_password)
        response = self.dm_api_account.account_api.put_v1_account_password(
            change_password=change_password, headers=token_header
        )
        return response

    @allure.step("Завершить сессию текущего авторизованного пользователя")
    def logout_user(
            self
    ):
        """
        Завершить сессию текущего авторизованного пользователя
        :return:
        """
        response = self.dm_api_account.login_api.delete_v1_account_login()
        return response

    @allure.step("Завершить все сессии текущего авторизованного пользователя")
    def logout_user_from_all_devices(
            self
    ):
        """
        Завершить все сессии текущего авторизованного пользователя
        :return:
        """
        response = self.dm_api_account.login_api.delete_v1_account_login_all()
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

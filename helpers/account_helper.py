from json import loads

from requests import Response

from services.api_mailhog import MailHog
from services.dm_api_account import DMApiAccount


class AccountHelper:
    def __init__(
            self,
            dm_api_account: DMApiAccount,
            mailhog: MailHog
    ):
        self.dm_api_account = dm_api_account
        self.mailhog = mailhog

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
        # Активировать пользователя
        response = self.activate_user_by_login(login=login)
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

    def user_login_forbidden(self,
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


    def activate_user_by_login(
            self,
            login: str
    ) -> Response:
        """
        Активировать пользователя по его логину
        :param login:
        :return:
        """
        # Получить письма из почтового сервера
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены."

        # Получить активационный токен из письма
        token = self._get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен для пользователя {login} не был получен."

        # Активировать пользователя
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован."

        return response

    @staticmethod
    def _get_activation_token_by_login(
            login: str,
            response: Response
    ) -> str:
        """
        Получить активационный токен для пользователя по его логину из списка писем
        :param login: логин пользователя
        :param response: ответ на запрос списка писем
        :return: активационный токен
        """
        token = None
        for item in response.json()["items"]:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        return token

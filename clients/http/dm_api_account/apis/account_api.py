import allure
from requests import Response

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from clients.http.dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step("Зарегистрировать нового пользователя")
    def post_v1_account(
            self,
            registration: Registration
    ) -> Response:
        """
        Register new user
        :param registration:
        :return:
        """
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def get_v1_account(
            self,
            validate_response: bool = True,
            **kwargs
    ) -> UserDetailsEnvelope | Response:
        """
        Get current user
        :param validate_response:
        :param kwargs:
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Активировать пользователя")
    def put_v1_account_token(
            self,
            token,
            validate_response: bool = True
    ) -> UserEnvelope | Response:
        """
        Activate registered user
        :param token:
        :param validate_response:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}'
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response: bool = True
    ) -> UserEnvelope | Response:
        """
        Change registered user email
        :param change_email:
        :param validate_response:
        :return:
        """
        response = self.put(
            path='/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сбросить пароль пользователя")
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response: bool = True
    ) -> UserEnvelope | Response:
        """
        Reset registered user password
        :param reset_password:
        :param validate_response:
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Установить новый пароль пользователя")
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            headers,
            validate_response: bool = True
    ) -> UserEnvelope | Response:
        """
        Change registered user password
        :param change_password:
        :param headers:
        :param validate_response:
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

import allure
from requests import Response

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response: bool = True
    ) -> UserEnvelope | Response:
        """
        Authenticate via credentials
        :param login_credentials:
        :param validate_response:
        :return:
        """
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def delete_v1_account_login(
            self
    ) -> Response:
        """
        Logout as current user
        :return:
        """
        response = self.delete(
            path='/v1/account/login'
        )
        return response

    def delete_v1_account_login_all(
            self
    ) -> Response:
        """
        Logout from every device
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all'
        )
        return response

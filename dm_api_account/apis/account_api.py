from requests import Response

from dm_api_account.models.registration import Registration
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

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
            **kwargs
    ):
        """
        Get current user
        :param kwargs:
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return response

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
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/email',
            json=json_data
        )
        return response

    def post_v1_account_password(
            self,
            json_data
    ):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=json_data
        )
        return response

    def put_v1_account_password(
            self,
            json_data,
            headers
    ):
        """
        Change registered user password
        :param json_data:
        :param headers:
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=json_data,
            headers=headers
        )
        return response

    def delete_v1_account_login(
            self
    ):
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
    ):
        """
        Logout from every device
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all'
        )
        return response

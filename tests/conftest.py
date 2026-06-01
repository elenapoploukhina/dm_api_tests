import datetime
from collections import namedtuple

import pytest
import structlog

from data.constants import (
    AUTH_CLIENT_USER_LOGIN,
    AUTH_CLIENT_USER_PASSWORD,
)
from helpers.account_helper import AccountHelper
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


@pytest.fixture(scope="session")
def mailhog_api():
    mail_hog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025")
    mailhog = MailHog(mail_hog_configuration)
    return mailhog


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_api_account=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope="session")
def auth_account_helper(
        mailhog_api
):
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog=mailhog_api)
    account_helper.auth_client(login=AUTH_CLIENT_USER_LOGIN, password=AUTH_CLIENT_USER_PASSWORD)
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    now_str = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
    login = f'lenaivanova_{now_str}'
    email = f'{login}@mail.ru'
    password = '123456789'
    User = namedtuple('User', ['login', 'email', 'password'])
    user = User(login=login, email=email, password=password)
    return user

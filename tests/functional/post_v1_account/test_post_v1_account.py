import pytest
import structlog

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


@pytest.fixture
def mailhog_api():
    mail_hog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025")
    mailhog = MailHog(mail_hog_configuration)
    return mailhog


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051")
    account = DMApiAccount(dm_api_configuration)
    return account


@pytest.fixture
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_api_account=account_api, mailhog=mailhog_api)
    return account_helper


def test_post_v1_account(
        account_helper
        ):
    login = 'lenaivanova_94'
    email = f'{login}@mail.ru'
    password = '123456789'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

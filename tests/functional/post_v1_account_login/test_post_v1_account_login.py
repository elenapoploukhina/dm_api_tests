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


def test_post_v1_account_login():
    mail_hog_configuration = MailhogConfiguration(host="http://185.185.143.231:5025")
    dm_api_configuration = DmApiConfiguration(host="http://185.185.143.231:5051", disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    mailhog = MailHog(mail_hog_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog=mailhog)

    login = 'lenaivanova_61'
    email = f'{login}@mail.ru'
    password = '123456789'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

import datetime
import os
from collections import namedtuple
from pathlib import Path

import pytest
import structlog
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v

from data.constants import (
    LOGIN_START_PART,
)
from helpers.account_helper import AccountHelper
from packages.restclient.configuration import Configuration as DmApiConfiguration
from packages.restclient.configuration import Configuration as MailhogConfiguration
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

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
    'telegram.chat_id',
    'telegram.bot_token'
)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host=v.get('service.dm_api_account'))
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    reporter.cleanup_input_files()


@pytest.fixture(scope="session", autouse=True)
def set_config(
        request
):
    config_path = Path(__file__).resolve().parents[1].joinpath("config")
    config_name = request.config.getoption("--env")
    # Локально данные берутся из локального конфига
    local_config = f"{config_name}.local"
    if (config_path / f"{local_config}.yaml").is_file():
        config_name = local_config
    v.set_config_name(config_name)
    v.add_config_path(config_path)
    v.read_in_config()

    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))

    if not os.getenv("TELEGRAM_BOT_CHAT_ID"):
        os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    if not os.getenv("TELEGRAM_BOT_ACCESS_TOKEN"):
        os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.bot_token")

    request.config.stash['telegram-notifier-addfields']['environment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = "https://elenapoploukhina.github.io/dm_api_tests"


def pytest_addoption(
        parser
):
    parser.addoption("--env", action="store", default="stg", help="run_stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope="session")
def mailhog_api():
    mail_hog_configuration = MailhogConfiguration(host=v.get('service.mailhog'))
    mailhog = MailHog(mail_hog_configuration)
    return mailhog


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
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
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog=mailhog_api)
    account_helper.auth_client(login=v.get('user.login'), password=v.get('user.password'))
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    now_str = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
    login = f'{LOGIN_START_PART}_{now_str}'
    email = f'{login}@mail.ru'
    password = v.get('user.password')
    User = namedtuple('User', ['login', 'email', 'password'])
    user = User(login=login, email=email, password=password)
    return user

import os
from pathlib import Path

from telebot import TeleBot
from vyper import v

config_path = Path(__file__).resolve().parents[2].joinpath("config")
config_name = ("prod")
local_config = f"{config_name}.local"
if (config_path / f"{local_config}.yaml").is_file():
    config_name = local_config
v.set_config_name(config_name)
v.add_config_path(config_path)
v.read_in_config()


def send_file() -> None:
    token = os.getenv("TELEGRAM_BOT_ACCESS_TOKEN") or v.get("telegram.bot_token")
    telegram_bot = TeleBot(token=token)
    file_path = Path(__file__).resolve().parents[2].joinpath('swagger-coverage-report-dm-api-account.html')
    with open(file_path, 'rb') as document:
        chat_id = os.getenv("TELEGRAM_BOT_CHAT_ID") or v.get("telegram.chat_id")
        telegram_bot.send_document(
            chat_id=chat_id,
            document=document,
            caption="Coverage"
        )


if __name__ == "__main__":
    send_file()

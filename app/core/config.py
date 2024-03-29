import os
from telebot.async_telebot import AsyncTeleBot


from pydantic import BaseSettings


class Settings(BaseSettings):
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "app")
    db_prefix = os.getenv("DB_PREFIX", "postgresql")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "token")
    SQLALCHEMY_DATABASE_URL = \
        f"{db_prefix}://{user}:{password}@{server}/{db}"
    TEST_SQLALCHEMY_DATABASE_URL = \
        f"{db_prefix}://{user}:{password}@{server}/test"
    EASTER_EGG_TEXT = os.getenv("EASTER_EGG_TEXT", "EASTER_EGG_TEXT")
    EASTER_EGG_RESPONSE = os.getenv(
        "EASTER_EGG_RESPONSE",
        "EASTER_EGG_RESPONSE",
    )


settings = Settings()

bot = AsyncTeleBot(settings.TELEGRAM_TOKEN, parse_mode=None)

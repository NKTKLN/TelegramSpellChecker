"""Module for application configuration.

Contains the Config class for loading settings from environment variables.
Allows management of database parameters, pagination, and external resources.
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Configuration class for loading settings from environment variables.

    Attributes:
        TELEGRAM_API_ID (str): Telegram API ID from environment variables.
        TELEGRAM_API_HASH (str): Telegram API Hash from environment variables.
    """

    # Environment variables
    TELEGRAM_API_ID: str
    TELEGRAM_API_HASH: str

    # Configuration for loading environment variables from .env file
    model_config = ConfigDict(env_file=".env")  # type: ignore
    _ = model_config


# Global instance of Config used throughout the application
config: Config = Config()  # type: ignore[call-arg]

"""Main entry point for the Telegram user bot that checks user messages for mistakes.

Initializes the Pyrogram client, sets up logging, configures the application,
and starts the bot.
"""

import argparse
import asyncio
import logging

from pyrogram import Client

from app.config import config
from app.logger import setup_logger

# Initialize logger for this module
logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to start the Telegram user bot.

    Initializes the Pyrogram client with API credentials from the config,
    registers message handlers, and runs the application.

    Supports a `--login` argument to authorize only without full launch.
    """
    parser = argparse.ArgumentParser(description="Telegram Spell Checker Bot")
    parser.add_argument(
        "--login", action="store_true", help="Authorize only, no full bot launch."
    )
    args = parser.parse_args()

    setup_logger(disable_logging=args.login)

    app = Client(
        "telegram-spell-checker",
        api_id=config.TELEGRAM_API_ID,
        api_hash=config.TELEGRAM_API_HASH,
    )

    if args.login:

        async def login_only():
            """Authorize the user without starting the bot."""
            await app.start()
            print("Authorization successful, session created.")
            await app.stop()

        asyncio.run(login_only())
        return

    logger.info("Registering handlers and starting bot")
    from app.handlers import Handlers

    Handlers(app)
    app.run()


if __name__ == "__main__":
    main()

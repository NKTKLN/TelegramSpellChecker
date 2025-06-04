"""Module for handling Telegram user messages and spell checking.

Implements message handlers for activating, deactivating, checking status,
and correcting spelling mistakes in user messages using LanguageTool.
"""

import logging

from language_tool_python import LanguageTool
from language_tool_python.utils import correct
from pyrogram import filters
from pyrogram import handlers as pyrogram_handlers
from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

# Initialize logger for this module
logger = logging.getLogger(__name__)


class Handlers:
    """A class to manage message handlers for the Telegram bot.

    Handles activation/deactivation, status reporting, and automatic correction
    of user messages using LanguageTool. Registers command and message handlers
    with the Pyrogram client.

    Attributes:
        app (Client): The Pyrogram client instance.
        is_active (bool): Current activation state of the bot.
        language_tool (LanguageTool): Instance of LanguageTool for Russian text.
    """

    def __init__(self, app: Client) -> None:
        """Initialize the Handlers with a Pyrogram client.

        Args:
            app (Client): The Pyrogram client instance used for handling messages.
        """
        self.app: Client = app
        self.is_active: bool = True
        self.language_tool: LanguageTool = LanguageTool("ru-RU")
        self.register_handlers()

    async def start_handler(self, _: Client, message: Message) -> None:
        """Activate the bot when the user sends `!start`.

        Args:
            _ (Client): Pyrogram client instance.
            message (Message): Incoming message object.
        """
        self.is_active = True
        logger.info("Bot activated.")
        await message.edit_text(
            "✅ <b>Bot is active!</b>\nNow all your messages will be checked for \
<b>mistakes</b>.",
            parse_mode=ParseMode.HTML,
        )

    async def stop_handler(self, _: Client, message: Message) -> None:
        """Deactivate the bot when the user sends `!stop`.

        Args:
            _ (Client): Pyrogram client instance.
            message (Message): Incoming message object.
        """
        self.is_active = False
        logger.info("Bot deactivated.")
        await message.edit_text(
            "🛑 <b>Bot is inactive!</b>\nSend <code>!start</code> to activate message \
checking again.",
            parse_mode=ParseMode.HTML,
        )

    async def status_handler(self, _: Client, message: Message) -> None:
        """Show current bot status when the user sends `!status`.

        Args:
            _ (Client): Pyrogram client instance.
            message (Message): Incoming message object.
        """
        status_text = "✅ <b>Active</b>" if self.is_active else "🛑 <b>Inactive</b>"
        logger.info("Status requested: %s", status_text)
        await message.edit_text(status_text, parse_mode=ParseMode.HTML)

    async def message_handler(self, _: Client, message: Message) -> None:
        """Process incoming messages and correct spelling errors if bot is active.

        Args:
            _ (Client): Pyrogram client instance.
            message (Message): Incoming message object.
        """
        if not self.is_active:
            logger.debug("Message received but bot is inactive, ignoring.")
            return

        logger.info("Processing message: %s", message.text.markdown)
        matches = self.language_tool.check(message.text.markdown)
        corrected_text = correct(message.text.markdown, matches)

        logger.info("Corrected message: %s", corrected_text)

        if corrected_text == message.text.markdown:
            logger.debug("No mistakes found in the message.")
            return

        await message.edit_text(corrected_text, parse_mode=ParseMode.MARKDOWN)

    def register_handlers(self) -> None:
        """Register command and message handlers with the Pyrogram client.

        Commands supported:
            !start — activate the bot
            !stop — deactivate the bot
            !status — check current status
        Also handles regular text messages from the user.
        """
        basic_filter = filters.text & filters.user("me")

        self.app.add_handler(
            pyrogram_handlers.MessageHandler(
                self.start_handler,
                filters.command("start", prefixes="!") & basic_filter,
            )
        )

        self.app.add_handler(
            pyrogram_handlers.MessageHandler(
                self.stop_handler, filters.command("stop", prefixes="!") & basic_filter
            )
        )

        self.app.add_handler(
            pyrogram_handlers.MessageHandler(
                self.status_handler,
                filters.command("status", prefixes="!") & basic_filter,
            )
        )

        self.app.add_handler(
            pyrogram_handlers.MessageHandler(self.message_handler, basic_filter)
        )
        logger.info("Handlers registered.")

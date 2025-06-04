"""Logging configuration module for the application.

Provides a setup_logger function to configure logging output to file or console,
as well as the ability to fully disable logging. Used to control diagnostic
information output during runtime.
"""

import logging


def setup_logger(
    disable_logging: bool = False, log_level: int = logging.INFO, log_file: str = ""
) -> None:
    """Configure the logging system for the application.

    Sets up basic logging configuration with the ability to output logs to either
    console or a file. Supports full logging disable when needed.

    Args:
        disable_logging (bool): Flag to disable all logging. If True, all logging
            will be disabled at CRITICAL level. Defaults to False.
        log_level (int): The severity level of messages to log. Acceptable values:
            logging.DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaults to logging.INFO.
        log_file (str): Path to the file where logs should be written. If empty or None,
            logs are printed to the console. Defaults to empty string.
    """
    if disable_logging:
        logging.disable(logging.CRITICAL)
        return

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level, format=log_format, filename=log_file, filemode="a"
    )

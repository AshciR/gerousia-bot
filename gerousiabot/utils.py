import logging
import os

from dotenv import load_dotenv


def setup_logger() -> logging.Logger:
    """
    Creates and configures a logger that will log
    to both the console and a file (file.log)
    :rtype: object the configured logger
    """
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('file.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def get_env_variable(key) -> str:
    """
    Gets the API token for a given key
    :param key: the key for the token you want returned
    :return: the API token
    """
    load_dotenv()  # Needed to run the application via the IDE
    return os.getenv(key)

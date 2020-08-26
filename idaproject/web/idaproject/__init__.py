import os

from library.api.api import API


DEFAULT_CONFIG_DIRECTORY = os.getcwd()
DEFAULT_DATABASE_URL = ''.join(["sqlite:///",
                                DEFAULT_CONFIG_DIRECTORY,
                                "temp.db"])


def get_api():
    return API(DEFAULT_DATABASE_URL)

import logging
from dataclasses import dataclass
from requests import Session, get

import constants
from lib.api.api_session import ApiSession


@dataclass
class ApiConfig:
    base_url: str = constants.URL
    common_api_url: str = constants.COMMON_API_URL


class ApiClient(Session):
    LOGGER = logging.getLogger("api_session")

    def __init__(self):
        self.base_url = ApiConfig.base_url
        self.common_api_url = ApiConfig.common_api_url
        self.api = ApiSession(self.base_url)
        self.common_api = ApiSession(self.common_api_url)

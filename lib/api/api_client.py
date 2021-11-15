import logging
from dataclasses import dataclass
from requests import Session, get
from lib.api.api_session import ApiSession


@dataclass
class ApiConfig:
    base_url: str = "https://search.rozetka.com.ua"


class ApiClient(Session):
    LOGGER = logging.getLogger("api_session")

    def __init__(self):
        self.base_url = ApiConfig.base_url
        self.api = ApiSession(self.base_url)

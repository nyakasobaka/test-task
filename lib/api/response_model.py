from json import JSONDecodeError
from typing import Optional, Any

from requests import Response


class ResponseModel:
    def __init__(self, resp):
        self.resp_obj: Response = resp
        self.status_code: int = resp.status_code
        self.payload: Optional[Any] = self._get_payload()
        self.error: Optional[Any] = self._extract_error()
        self.data: Optional[Any] = self._get_data()

    def _get_payload(self):
        try:
            return self.resp_obj.json()
        except JSONDecodeError:
            return self.resp_obj.text

    def _get_data(self):
        if isinstance(self.payload, dict):
            return self.payload.get("data")
        return None

    def _extract_error(self):
        if self.status_code < 400:
            return None
        if isinstance(self.payload, dict):
            return self.payload.get("errors", self.payload)
        return self.payload
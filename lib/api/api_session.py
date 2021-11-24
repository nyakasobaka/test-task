import logging
from urllib.parse import urlparse, urljoin

import requests
from allure_commons._allure import step
from requests import Session

from lib.allure_pytest_bdd.http_attachment import http_attachment, MakoAttachmentRenderer, add_attachment
from lib.api.response_model import ResponseModel

LOGGER = logging.getLogger("api_session")


class ApiSession(Session):

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, data=None, headers=None, json=None, **kwargs):
        headers = headers if headers is not None else {}
        headers["Cache-Control"] = "no-cache"
        url = self._build_url(url)

        def internal_request():
            LOGGER.info(f"Request: [{method}: {url}]")
            LOGGER.debug(f"Request body: [{data}]")

            response = super(ApiSession, self).request(method=method, url=url, headers=headers, json=json, data=data,
                                                       **kwargs)
            self._attach_request_artifacts(response.request, response)
            LOGGER.info(f"Response: code: [{response.status_code}]")
            LOGGER.debug(f"Response text: [{response.text}] reason: [{response.reason}]")
            _resp = ResponseModel(response)
            return _resp
        return internal_request()

    def _build_url(self, path):
        """ prepend url with hostname unless it's already an absolute URL """
        return path if bool(urlparse(path).netloc) else urljoin(self.base_url, path)

    @staticmethod
    def _attach_request_artifacts(request: requests.PreparedRequest, response: requests.Response):
        """Building http attachments with payloads using mako templates from allure_pytest_bdd folder"""
        builder = http_attachment("Request")
        builder.add_url(request.url)
        builder.add_method(request.method)
        builder.add_headers(dict(request.headers))
        builder.add_body(request.body or "")

        add_attachment(builder.build(), MakoAttachmentRenderer("http-request.mak"))

        builder = http_attachment("Response")
        builder.add_response_code(response.status_code)
        builder.add_headers(dict(response.headers))
        builder.add_cookies(dict(response.cookies))
        builder.add_body(response.text or "")

        add_attachment(builder.build(), MakoAttachmentRenderer("http-response.mak"))


import pytest

from data_for_tests.context import Context
from lib.api.api_client import ApiClient
from lib.api.api_facade import APIFacade


def pytest_addoption(parser):
    parser.addoption("-B", "--browser", dest="browser", action="append",
                     help="Specify Browser(s). Valid options are: chrome, edge, firefox, ie, opera, safari")

    parser.addoption("-H", "--host", dest="host", action="store", help="Specify remote host(s) with selenoid.",
                     default="localhost")

    parser.addoption("-P", "--port", dest="port", action="store", help="Specify port selenoid listens.", default="4444")


@pytest.fixture(scope="module")
def api():
    api_client = ApiClient()
    return APIFacade(api_client)


@pytest.fixture(scope="module")
def context():
    return Context()

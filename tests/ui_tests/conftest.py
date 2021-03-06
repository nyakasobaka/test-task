import pytest
from pytest_bdd import given

from helpers.ui_helpers.attachment_helper import attach_png
from helpers.ui_helpers.session_config import SessionConfiguration
from helpers.ui_helpers.ui_facade import UiFacade
import helpers.ui_helpers.driver_manager as DriverManager


def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        metafunc.parametrize("browser", SessionConfiguration.browsers)


def pytest_configure(config):
    param_browsers_list = config.getoption("-B") or ["chrome"]
    host = config.getoption("-H")
    port = config.getoption("-P")

    SessionConfiguration.browsers = sorted(param_browsers_list) or []
    SessionConfiguration.selenoid_host = host or "localhost"
    SessionConfiguration.selenoid_port = port or 4444


@pytest.fixture(scope="function")
def ui_test_fixture(request, browser):
    """
    Test fixture to initialize driver
    """
    test_name = request.node.name
    selenoid_host = request.config.getoption("-H")
    selenoid_port = request.config.getoption("-P")
    driver = None
    additional_caps = {"enableVideo": False}
    additional_caps["name"] = test_name
    driver = DriverManager.get_driver(
        browser=browser,
        additional_caps=additional_caps,
        host=selenoid_host,
        port=selenoid_port
    )
    yield driver
    try:
        screenshot = driver.get_screenshot_as_png()
        attach_png(screenshot)
    except:
        pass
    try:
        driver.quit()
    except:
        pass


@pytest.fixture(scope="function")
def ui_app(ui_test_fixture) -> UiFacade:
    return UiFacade(ui_test_fixture)


@given("main page opened")
def main_page_loaded(ui_app):
    ui_app.pages.open_main_page().goods_grid.wait_for_grid_loaded()

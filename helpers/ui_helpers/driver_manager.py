import json
import os
import platform

import urllib3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as InternetExplorerOptions
from selenium.webdriver.opera.options import Options as OperaOptions

from constants import CAPABILITIES_DIRECTORY


def options(browser):
    if browser == "firefox":
        _options = FirefoxOptions()
        _options.set_preference("browser.download.folderList", 2)
        _options.set_preference("browser.download.manager.showWhenStarting", False)
        # _options.set_preference("browser.download.dir", save_to_path)
        _options.set_preference("browser.download.dir", "/home/selenium/Downloads/")
        _options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    elif browser == "chrome":
        _options = ChromeOptions()
        _options.add_argument("disable-infobars")
        _options.add_argument("disable-extensions")
        _options.add_argument("disable-web-security")
        _options.add_argument("allow-running-insecure-content")
        _options.add_argument("safebrowsing-disable-extension-blacklist")
        _options.add_argument("safebrowsing-disable-download-protection")
        _options.add_argument("disable-popup-blocking")
    elif browser == "opera":
        _options = OperaOptions()
    else:
        raise ValueError(browser + " not supported")
    return _options


def capabilities(browser):
    _capabilities = {}
    general_caps = os.path.join(CAPABILITIES_DIRECTORY, "general_caps.json")
    with open(general_caps, "r") as readfile:
        caps_json = json.loads(readfile.read())
        for cap in caps_json["capabilities"]:
            _capabilities.update({cap: caps_json["capabilities"][cap]})
    os_name = platform.system().lower()
    platform_dir = os.path.join(CAPABILITIES_DIRECTORY, os_name, "")
    platform_caps = os.path.join(platform_dir, os_name + ".json")
    with open(platform_caps, "r") as readfile:
        caps_json = json.loads(readfile.read())
        for cap in caps_json["capabilities"]:
            _capabilities.update({cap: caps_json["capabilities"][cap]})
    browser_caps = os.path.join(platform_dir + browser + ".json")
    with open(browser_caps, "r") as readfile:
        caps_json = json.loads(readfile.read())
        for cap in caps_json["capabilities"]:
            _capabilities.update({cap: caps_json["capabilities"][cap]})
    return _capabilities


def get_driver(browser, additional_caps, host, port):
    http_prefix = "" if "http" in host else "http://"
    executor = f"{http_prefix}{host}:{port}/wd/hub"
    caps = capabilities(browser)
    opt = options(browser)
    if additional_caps is not None:
        caps.update(additional_caps)
    try:
        driver = webdriver.Remote(desired_capabilities=caps, command_executor=executor, options=opt)
    except urllib3.exceptions.ProtocolError as err:
        print("Failed to connect to remote driver, reconnecting...")
        raise err
    except WebDriverException as _exception:
        if "No such image:" in _exception.msg:
            image_name = _exception.msg.split("No such image: ")[-1]
            print(_exception.msg, f"\nPulling image: {image_name}")
            os.system(f"docker pull {image_name}")
        raise _exception
    driver.set_window_size(1920, 1080)
    return driver
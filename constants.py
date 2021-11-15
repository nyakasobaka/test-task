import os

DEFAULT_PAGE_LOAD_TIMEOUT = 30

URL = "https://search.rozetka.com.ua"
UI_URL = "https://hard.rozetka.com.ua"
PROJECT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
CAPABILITIES_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "tests", "ui_tests", "capabilities")
TESTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "tests")
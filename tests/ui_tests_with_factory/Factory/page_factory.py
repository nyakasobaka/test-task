from enum import Enum

from tests.ui_tests_with_factory.pages.rozetka_base_page import RozetkaBasePage
from tests.ui_tests_with_factory.pages.search_results_page import SearchResultsPage


class PageType(Enum):
    MainPage = "MainPage"
    SearchPage = "SearchPage"


class Factory:
    def __init__(self, driver):
        self.driver = driver

    def get_page(self, page: PageType):
        if page == PageType.SearchPage:
            return SearchResultsPage(self.driver)
        elif page == PageType.MainPage:
            return RozetkaBasePage(self.driver)

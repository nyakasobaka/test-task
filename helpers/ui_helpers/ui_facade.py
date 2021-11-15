from helpers.ui_helpers.ui_facade_object import UiApp
from tests.ui_tests.pages.rozetka_base_page import RozetkaBasePage
from tests.ui_tests.pages.search_results_page import SearchResultsPage
from tests.ui_tests.url_navigation.navigation import Navigation


class UiFacade:
    def __init__(self, driver):
        self.ui_app = UiApp(driver, self)
        self.common_steps = CommonSteps(self.ui_app)
        self.pages = Pages(self.ui_app)
        self.url_navigation = UrlNavigation(self.ui_app)


class CommonSteps:
    def __init__(self, app: UiApp):
        from tests.ui_tests.common_steps.search_steps import SearchSteps
        self.search_steps = SearchSteps(app)


class Pages(RozetkaBasePage):
    def __init__(self, app: UiApp):
        super().__init__(app)
        self.search_results_page = SearchResultsPage(app)


class UrlNavigation(RozetkaBasePage):
    def __init__(self, app: UiApp):
        super().__init__(app)
        self.navigation = Navigation(app)

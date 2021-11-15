from urllib.parse import urlparse

from allure_commons._allure import step

from tests.ui_tests.pages.base_page import BasePage


class Navigation(BasePage):

    def __init__(self, app):
        super().__init__(app)
        self.driver = app.driver

    @step("Navigates to selected page")
    def navigate_to(self, page, *args):
        """
        Opens given url
        url can contains  additional elements which describes via double curly braces in  UrlsStore string
        :param page: UrlsStore string, can contains elements that will be replaced elements from args
        :param args:optional strings,  part of url ( id, name of item)
        """
        url = urlparse(self.driver.current_url)
        self.go_to(f"{url.scheme}://{url.netloc}/{page.format(*args)}")

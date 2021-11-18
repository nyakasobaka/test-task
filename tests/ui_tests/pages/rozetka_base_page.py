from selenium.webdriver.common.by import By

import constants
from tests.ui_tests.pages.base_page import BasePage
from tests.ui_tests.pages.element import Element, Grid


class RozetkaBasePage(BasePage):
    search_input_locator = (By.XPATH, "//input[@name='search']")
    search_button_locator = (By.XPATH, "//button[contains(@class,'search-form__submit')]")

    def __init__(self, conf):
        super().__init__(conf)
        self.search_input = Element(self.driver, self.search_input_locator)
        self.search_button = Element(self.driver, self.search_button_locator)
        self.goods_grid = Grid(self.driver)

    def open_main_page(self):
        self.go_to(constants.UI_URL)
        return self

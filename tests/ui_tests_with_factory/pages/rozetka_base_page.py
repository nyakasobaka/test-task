import constants
from tests.ui_tests_with_factory.pages.base_page import BasePage
from tests.ui_tests_with_factory.pages.element import Grid, TopMenuPanel


class RozetkaBasePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.goods_grid = Grid(self.driver)
        self.top_menu = TopMenuPanel(self.driver)

    def open_main_page(self):
        self.go_to(constants.UI_URL)
        return self

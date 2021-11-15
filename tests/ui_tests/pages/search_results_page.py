from selenium.webdriver.common.by import By

from tests.ui_tests.pages.base_page import BasePage
from tests.ui_tests.pages.element import Grid, Element


class SearchResultsPage(BasePage):
    grid_locator = (By.XPATH, "//div[@class='layout layout_with_sidebar']")
    header_text_locator = (By.XPATH, "//h1")

    def __init__(self, conf):
        super().__init__(conf)
        self.search_results_grid = Grid(self.driver, self.grid_locator)
        self.header_text = Element(self.driver, self.header_text_locator)

    def get_header_text(self) -> str:
        return self.header_text.text


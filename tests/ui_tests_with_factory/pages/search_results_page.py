from assertpy import assert_that
from selenium.webdriver.common.by import By

from helpers.retry_helper import retry
from tests.ui_tests_with_factory.pages.base_page import BasePage
from tests.ui_tests_with_factory.pages.element import Grid, Element, TopMenuPanel
from tests.ui_tests_with_factory.pages.filter import CategoryFilterComponent, FilterPanelDecorator, \
    PriceFilterComponent, PriceFilterDecorator, ProducerFilterComponent


class SearchResultsPage(BasePage):
    grid_locator = (By.XPATH, "//div[@class='layout layout_with_sidebar']")
    header_text_locator = (By.XPATH, "//h1")

    def __init__(self, driver):
        super().__init__(driver)
        self.search_results_grid = Grid(self.driver, self.grid_locator)
        self.header_text = Element(self.driver, self.header_text_locator)
        self.top_menu = TopMenuPanel(self.driver)
        self.categories = CategoryFilterComponent(self.driver)
        self.producers = ProducerFilterComponent(self.driver)
        self.prices = PriceFilterComponent(self.driver)

    def set_category(self, category):
        FilterPanelDecorator(self.categories).select_filter(category)
        return self

    @retry(tries=4, delay=2)
    def set_producer(self, producer):
        FilterPanelDecorator(self.producers).select_filter(producer)
        return self


    def get_header_text(self) -> str:
        return self.header_text.text

    def click_search_button(self):
        self.top_menu.click_search_button()
        return self

    def submit_price(self):
        PriceFilterDecorator(self.prices).select_filter()
        self.search_results_grid.wait_for_grid_loaded()
        return self

    def get_all_found_goods_on_page(self):
        return self.search_results_grid.get_all_grid_items()

    def get_goods_item_by_title_containing_text(self, text):
        return self.search_results_grid.get_item_by_title(text)

    def set_min_price(self, price):
        PriceFilterDecorator(self.prices).set_min_price(price)
        return self

    def set_max_price(self, price):
        PriceFilterDecorator(self.prices).set_max_price(price)
        return self

    def get_total_amount_of_goods(self) -> str:
        return self.search_results_grid.total_amount.text

    def validate_header_text(self, search_text: str):
        actual_text = self.get_header_text()[1:-1]
        assert_that(actual_text.lower()).is_equal_to(search_text.lower())

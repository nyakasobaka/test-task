from selenium.common.exceptions import MoveTargetOutOfBoundsException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from helpers.retry_helper import retry
from tests.ui_tests.pages.base_page import BasePage
from tests.ui_tests.pages.element import Grid, Element
from tests.ui_tests.pages.filter import PriceFilterDecorator, CategoryFilterComponent, ProducerFilterComponent, \
    PriceFilterComponent, FilterPanelDecorator


class SearchResultsPage(BasePage):
    grid_locator = (By.XPATH, "//div[@class='layout layout_with_sidebar']")
    header_text_locator = (By.XPATH, "//h1")

    def __init__(self, conf):
        super().__init__(conf)
        self.search_results_grid = Grid(self.driver, self.grid_locator)
        self.header_text = Element(self.driver, self.header_text_locator)
        self.categories = CategoryFilterComponent(self.driver)
        self.producers = ProducerFilterComponent(self.driver)
        self.prices = PriceFilterComponent(self.driver)

    def get_header_text(self) -> str:
        """get search results header text"""
        return self.header_text.text

    def set_category(self, category):
        """
        Select checkbox with category in left panel
        :param category: category to find and check
        :return: SearchResultsPage
        """
        FilterPanelDecorator(self.categories).select_filter(category)
        return self

    def submit_price(self):
        """
        click Ok button after prices are set in price section of filter
        :return: SearchResultsPage
        """
        PriceFilterDecorator(self.prices).select_filter()
        self.search_results_grid.wait_for_grid_loaded()
        return self

    @retry(tries=4, delay=2, exceptions=StaleElementReferenceException,
           action_before_retry=lambda: SearchResultsPage.driver.refresh())
    def set_producer(self, producer):
        """
        Select checkbox with producer in left panel
        :param producer: producer to search and select
        :return: SearchResultsPage
        """
        FilterPanelDecorator(self.producers).select_filter(producer)
        return self

    def set_min_price(self, price):
        """
        enter minimum price into input at price filter
        :param price: minimum price to set
        :return: SearchResultsPage
        """
        PriceFilterDecorator(self.prices).set_min_price(price)
        return self

    def set_max_price(self, price):
        """
        enter max price into input at price filter
        :param price: max price to set
        :return: SearchResultsPage
        """
        PriceFilterDecorator(self.prices).set_max_price(price)
        return self

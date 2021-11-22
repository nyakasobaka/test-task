# example of Decorator pattern. There is no need in it here, but task requires using it somewhere
from abc import abstractmethod

from selenium.webdriver.common.by import By

from helpers.common_helpers import ignore_case_xpath
from tests.ui_tests.pages.element import Element


class FilterPanelComponent(Element):
    filter_panel_locator = (By.XPATH, "//aside[contains(@class,'sidebar')]")

    def __init__(self, driver, locator=filter_panel_locator):
        super().__init__(driver, locator)

    @abstractmethod
    def select_filter(self, filter_text):
        pass


class CategoryFilterComponent(FilterPanelComponent):
    filter_panel_locator = (By.XPATH, "//aside[contains(@class,'sidebar')]")

    def __init__(self, driver, locator=filter_panel_locator):
        super().__init__(driver, locator)

    def select_filter(self, filter_text):
        locator = (By.XPATH, f"//rz-filter-categories//span[contains(text(), '{filter_text}')]/parent::*")
        Element(self.driver, locator).click_with_js()


class SellerFilterComponent(FilterPanelComponent):
    filter_panel_locator_text = "//div[@data-filter-name='seller']"
    filter_panel_locator = (By.XPATH, filter_panel_locator_text)

    def __init__(self, driver, locator=filter_panel_locator):
        super().__init__(driver, locator)

    def select_filter(self, filter_text):
        locator = (By.XPATH, f"{self.filter_panel_locator_text}//input[{ignore_case_xpath('@id', filter_text)}]")
        elem = Element(self.driver, locator)
        elem.scroll_into_view()
        elem.click_with_js()


class ProducerFilterComponent(FilterPanelComponent):
    filter_panel_locator_text = "//div[@data-filter-name='producer']"
    filter_panel_locator = (By.XPATH, filter_panel_locator_text)

    def __init__(self, driver, locator=filter_panel_locator):
        super().__init__(driver, locator)

    def select_filter(self, filter_text):
        locator = (By.XPATH, f"{self.filter_panel_locator_text}//input[{ignore_case_xpath('@id', filter_text)}]")
        elem = Element(self.driver, locator)
        elem.scroll_into_view()
        elem.click_with_js()


class PriceFilterComponent(FilterPanelComponent):
    filter_panel_locator_text = "//div[@data-filter-name='price']"
    min_price_locator = (By.XPATH, "//input[@formcontrolname='min']")
    max_price_locator = (By.XPATH, "//input[@formcontrolname='max']")
    submit_price_button_locator = (By.XPATH, "//button[contains(@class,'slider-filter__button')]")
    filter_panel_locator = (By.XPATH, filter_panel_locator_text)

    def __init__(self, driver, loctor=filter_panel_locator):
        super().__init__(driver, loctor)
        self.min_price_input = Element(self.driver, self.min_price_locator)
        self.max_price_input = Element(self.driver, self.max_price_locator)
        self.submit_price_button = Element(self.driver, self.submit_price_button_locator)

    def select_filter(self, filter_text=None):
        self.submit_price_button.click()


class FilterPanelDecorator(FilterPanelComponent):
    _item_component: FilterPanelComponent

    def __init__(self, item: FilterPanelComponent):
        self._item_component = item

    def select_filter(self, filter_text=None):
        self._item_component.select_filter(filter_text)


class PriceFilterDecorator(FilterPanelDecorator):
    _item_component: PriceFilterComponent

    def __init__(self, item: PriceFilterComponent):
        super().__init__(item)
        self._item_component = item

    def set_min_price(self, price):
        self._item_component.min_price_input.send_keys(price)

    def set_max_price(self, price):
        self._item_component.max_price_input.send_keys(price)

from time import sleep

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    ElementNotSelectableException, StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

import constants
from helpers.common_helpers import ignore_case_xpath
from helpers.retry_helper import retry


class Element:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = tuple(locator[:2])
        self.description = (locator[2] if len(locator) > 2
                            else "Unknown name of element. Please describe the locator name.")

    @property
    def text(self):
        """finds element and returns the text"""
        return self.find_element().text

    def click_with_js(self):
        """clicks on element using JavaScript"""
        element = self.find_element()
        self.driver.execute_script("arguments[0].click();", element)

    def click(self, wait_to_be_clickable=True):
        """waits element to be clickable and clicks it, if wait_to_be_clickable parameter is False skips
         "wait to be clickable" check for element and just clicks it.
        :param wait_to_be_clickable skip "wait to be clickable" check for element
        :type wait_to_be_clickable bool
        """
        if wait_to_be_clickable:
            self.wait_for_clickable()
        self.find_element().click()

    def send_keys(self, text):
        """waits element to be clickable, clears input and sends text"""
        self.wait_for_clickable()
        element = self.find_element()
        element.clear()
        element.send_keys(text)

    def wait_for_clickable(self, timeout=constants.DEFAULT_PAGE_LOAD_TIMEOUT):
        """returns element in case element is displayed and is enabled"""
        element = self._wait(timeout).until(expected_conditions.element_to_be_clickable(self.locator))
        return element

    def find_element(self, timeout=constants.DEFAULT_PAGE_LOAD_TIMEOUT):
        """waits and returns element in case element was found"""
        return self._wait(timeout=timeout).until(expected_conditions.presence_of_element_located(self.locator))

    def find_elements(self, locator):
        """ finds elements in webelement"""
        return self.find_element().find_elements(*locator[:2])

    def _wait(self, timeout=constants.DEFAULT_PAGE_LOAD_TIMEOUT):
        """wait to use in custom waiters"""
        wait = WebDriverWait(driver=self.driver, timeout=timeout, ignored_exceptions=(
            NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException,
            StaleElementReferenceException, ElementClickInterceptedException))
        return wait

    def is_displayed(self, timeout=2):
        """
        Checks whether element is displayed on page
        :param timeout: time in seconds to wait until try to check whether is element is displayed on page
        :type timeout: int
        :return: <bool>
        """
        try:
            element = self.find_element(timeout=timeout)
            return element.is_displayed()
        except TimeoutException:
            return False

    def scroll_into_view(self, timeout=constants.DEFAULT_PAGE_LOAD_TIMEOUT):
        """
        Scrolls to element
        """
        if not self.is_displayed():
            element = self.find_element(timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.perform()
            sleep(0.1)
            # Fix for FF
            self.driver.execute_script("arguments[0].scrollIntoView();", element)


class GridItem(Element):
    grid_item_title_locator_text = "//span[@class='goods-tile__title']"
    grid_item_price_locator_text = "//span[@class='goods-tile__price-value']"
    grid_item_currency_locator_text = "//span[@class='goods-tile__price-currency']"
    grid_item_old_price_locator_text = "//div[contains(@class, 'goods-tile__price--old')]"

    def __init__(self, driver, locator):
        super().__init__(driver, locator)
        self.grid_item_title_locator = (By.XPATH, f"{locator[1]}{self.grid_item_title_locator_text}")
        self.grid_item_price_locator = (By.XPATH, f"{locator[1]}{self.grid_item_price_locator_text}")
        self.grid_item_currency_locator = (By.XPATH, f"{locator[1]}{self.grid_item_currency_locator_text}")
        self.grid_item_old_price_locator = (By.XPATH, f"{locator[1]}{self.grid_item_old_price_locator_text}")
        self.grid_item = Element(self.driver, locator)
        self.grid_item_title = Element(self.driver, self.grid_item_title_locator)
        self.grid_item_price = Element(self.driver, self.grid_item_price_locator)
        self.grid_item_currency = Element(self.driver, self.grid_item_currency_locator)
        self.grid_item_old_price = Element(self.driver, self.grid_item_old_price_locator)

    def get_old_price(self):
        """
        get item's price before discount
        :return: float price
        """
        price = self.grid_item_old_price.text.replace(" ", "")[:-1] if self.grid_item_old_price.text else 0
        return float(price)

    def get_price(self):
        """
        get item's price
        :return: float price
        """
        return float(self.grid_item_price.text.replace(" ", ""))

    def get_item_title(self):
        """
        get title of element in grid
        :return: grind item title
        """
        return self.grid_item_title.text


class TopMenuPanel(Element):
    search_input_locator = (By.XPATH, "//input[@name='search']")
    search_button_locator = (By.XPATH, "//button[contains(@class,'search-form__submit')]")
    menu_locator = (By.XPATH, "//div[@class='header-layout']")

    def __init__(self, driver, locator=menu_locator):
        super().__init__(driver, locator)
        self.search_input = Element(self.driver, self.search_input_locator)
        self.search_button = Element(self.driver, self.search_button_locator)

    def send_text_to_search_input(self, text: str):
        """
        enter text insearch input field without pressing search button
        :param text: text to enter
        :return:
        """
        self.search_input.send_keys(text)
        return self

    def click_search_button(self):
        """
        click search button
        :return:
        """
        self.search_button.click()


class Grid(Element):
    grid_locator = (By.XPATH, "//div[@class='layout layout_with_sidebar']")
    grid_item_locator = (By.XPATH, "//ul[contains(@class,'catalog-grid')]//li")
    pagination_list_locator = (By.XPATH, "//ul[@class='pagination__list']")
    filter_panel_locator = (By.XPATH, "//aside[contains(@class,'sidebar')]")
    total_amount_locator = (By.XPATH, "//p[contains(@class,'catalog-selection__label')]")
    seller_filtration_block_locator = (By.XPATH, "//div[@data-filter-name='seller']")
    ready_for_delivery_filtration_block_locator = (By.XPATH, "//div[@data-filter-name='gotovo-k-otpravke']")
    producer_filtration_block_locator = (By.XPATH, "//div[@data-filter-name='producer']")
    min_price_locator = (By.XPATH, "//input[@formcontrolname='min']")
    max_price_locator = (By.XPATH, "//input[@formcontrolname='max']")
    submit_price_button_locator = (By.XPATH, "//button[contains(@class,'slider-filter__button')]")

    def __init__(self, driver, locator=grid_locator):
        super().__init__(driver, locator)
        self.grid = Element(self.driver, locator)
        self.filter_panel = Element(self.driver, self.filter_panel_locator)
        self.seller_filtration_block = Element(self.driver, self.seller_filtration_block_locator)
        self.ready_for_delivery_filtration_block = Element(self.driver, self.ready_for_delivery_filtration_block_locator)
        self.producer_filtration_block = Element(self.driver, self.producer_filtration_block_locator)
        self.pagination_list = Element(self.driver, self.pagination_list_locator)
        self.total_amount = Element(self.driver, self.total_amount_locator)
        self.min_price_input = Element(self.driver, self.min_price_locator)
        self.max_price_input = Element(self.driver, self.max_price_locator)
        self.submit_price_button = Element(self.driver, self.submit_price_button_locator)

    @retry(tries=4, delay=2)
    def filter_by_checkbox(self, filter_text: str):
        """
        :param filter_text - click checkbox in filter panel by given text
        """
        locator = (By.XPATH, f"//input[{ignore_case_xpath('@id', filter_text)}]")
        elem = Element(self.driver, locator)
        elem.scroll_into_view()
        elem.click_with_js()

    @retry(tries=4, delay=2)
    def filter_by_category(self, cat_name):
        """
        :param cat_name: name of category
        """
        locator = (By.XPATH, f"//rz-filter-categories//span[contains(text(), '{cat_name}')]/parent::*")
        Element(self.driver, locator).click_with_js()

    def get_all_grid_items(self):
        """
        get all items from grid
        :return: list of items
        """
        return self.grid.find_elements(self.grid_item_locator)

    def is_checkbox_selected(self, filter_text: str):
        """
        check is filter checkbox is checked
        :param filter_text: checkbox with text which should be checked
        :return: bool is checkbox active
        """
        locator = (By.XPATH, f"//input[{ignore_case_xpath('@id', filter_text)}]")
        return Element(self.driver, locator).find_element(timeout=2).is_selected()

    def go_to_page_by_number(self, page_number: int):
        """
        pagination - go to page by number
        :param page_number:
        :return:
        """
        self.pagination_list.find_elements((By.XPATH, f"//a[contains(@href,'page={page_number}')]")).click()

    @retry(exceptions=TimeoutException, tries=5, delay=5)
    def wait_for_grid_loaded(self):
        """
        wait till grid loaded
        :return:
        """
        return self.grid.find_element(timeout=5)

    def get_item_by_title(self, title):
        """
        search item in grid by title
        :param title: title to search
        :return:
        """
        locator = (By.XPATH, f"//ul[contains(@class,'catalog-grid')]//a[contains(@title, '{title}')]/parent::*")
        return GridItem(self.driver, locator)




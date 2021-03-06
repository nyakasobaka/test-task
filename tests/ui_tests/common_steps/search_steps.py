from assertpy import assert_that

from helpers.ui_helpers.ui_facade import UiFacade


class SearchSteps:
    def __init__(self, app):
        self.driver = app.driver
        self.ui_app: UiFacade = app.ui_app

    def validate_header_text(self, search_text: str):
        """
        Check if header text equals to  expected
        :param search_text: expected text
        :return:
        """
        actual_text = self.ui_app.pages.search_results_page.get_header_text()[1:-1]
        assert_that(actual_text.lower()).is_equal_to(search_text.lower())

    def search_by_text(self, text: str):
        """
        Search by given text
        :param text: text to search
        :return:
        """
        self.ui_app.pages.search_input.send_keys(text)
        self.ui_app.pages.search_button.click()
        self.ui_app.pages.search_results_page.search_results_grid.wait_for_grid_loaded()

    def send_text_to_search_input(self, text: str):
        """ enter text into search input without pressing search button"""
        self.ui_app.pages.search_input.send_keys(text)

    def click_search_button(self):
        """click search button"""
        self.ui_app.pages.search_button.click()

    def get_all_found_goods_on_page(self):
        """
        get all good items from grid
        :return: list of elements
        """
        return self.ui_app.pages.search_results_page.search_results_grid.get_all_grid_items()

    def get_goods_item_by_title_containing_text(self, text):
        """
        get goods item with title equals given text
        :param text: title of element
        :return: element
        """
        return self.ui_app.pages.search_results_page.search_results_grid.get_item_by_title(text)

    def get_total_amount_of_goods(self)->str:
        """return total mount of goods shown in filter panel"""
        return self.ui_app.pages.search_results_page.search_results_grid.total_amount.text

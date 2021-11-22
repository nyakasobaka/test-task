from abc import ABC, abstractmethod

from assertpy import soft_assertions, assert_that

from models.goods_item_model import GoodsItemModel
from tests.ui_tests.pages.element import GridItem


class Strategy(ABC):

    @abstractmethod
    def check_price(self, api_elem, ui_elem):
        pass


class ValidationContext():
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy):
        self._strategy = strategy

    def validate_price(self, api_elem: GoodsItemModel, ui_elem: GridItem):
        self._strategy.check_price(api_elem, ui_elem)


class DiscountValidationStrategy(Strategy):
    def check_price(self, api_elem: GoodsItemModel, ui_elem: GridItem):
        """
        check api and ui old prices are equal
        check api and ui prices are equal
        :param ui_elem: Element to check price
        :param api_elem: api element to be compared
        :return: None
        """
        with soft_assertions():
            assert_that(ui_elem.get_price(), f"Price on ui is {ui_elem.get_price()} "
                                             f"and price from api is {api_elem.price}").is_equal_to(api_elem.price)
            assert_that(ui_elem.get_old_price(), f"old price on ui is {ui_elem.get_old_price()}"
                                                 f"and api old price is {api_elem.old_price}").is_equal_to(api_elem
                                                                                                           .old_price)


class PriceValidationStrategy(Strategy):
    def check_price(self, api_elem: GoodsItemModel, ui_elem: GridItem):
        """
        check old prise is 0
        check price equals to api
        :param ui_elem: GridItem element to check price
        :param api_elem: api element to be compared
        :return:
        """
        with soft_assertions():
            assert_that(ui_elem.get_old_price(), f"Old price is not 0, but {ui_elem.get_old_price()}").is_equal_to(0)
            assert_that(ui_elem.get_price(), f"Api price is {api_elem.price} "
                                             f"and ui price is {ui_elem.get_price()}").is_equal_to(api_elem.price)

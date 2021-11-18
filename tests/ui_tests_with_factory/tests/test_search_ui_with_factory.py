from assertpy import assert_that
from pytest_bdd import when, then, parsers, scenario
from copy import copy
from helpers.api_helpers import get_items_with_discount, get_items_without_discount
from tests.ui_tests_with_factory.common_steps.validation_strategy import PriceValidationStrategy
from tests.ui_tests_with_factory.common_steps.search_steps import serch_by_text
from tests.ui_tests_with_factory.common_steps.validation_strategy import ValidationContext, DiscountValidationStrategy


@when(parsers.parse('search by text {text}'))
def enter_text_into_search_input(ui_page, text, context):
    context.text = text
    serch_by_text(ui_page, text)


@then("click search button")
@when("click search button")
def click_search_button(ui_page):
    ui_page.top_menu.click_search_button()


@then("search results page contains correct header")
def check_search_results_header(search_page, context):
    search_page.validate_header_text(context.text)


@then(parsers.parse("filter {filter_item} is selected in filter panel"))
def verify_producer_is_selected_in_filter(search_page, filter_item):
    search_page.search_results_grid.wait_for_grid_loaded()
    assert_that(search_page.search_results_grid.is_checkbox_selected(filter_item)).is_true()


@when(parsers.parse("select filters {filters} in filter panel"))
def select_filter_item_in_filter(search_page, context, filters):
    search_page.search_results_grid.wait_for_grid_loaded()
    context.filters_list = filters.replace(" ", "").split(",")
    for filter_item in context.filters_list:
        search_page.set_producer(filter_item).search_results_grid.wait_for_grid_loaded()


@when(parsers.parse("set min price in filter panel to {price}"))
def se_min_price_in_filter(search_page, context, price):
    context["min_price"] = price
    search_page.set_min_price(price)


@when(parsers.parse("set max price in filter panel to {price}"))
def set_max_price_in_filter(search_page, context, price):
    context["max_price"] = price
    search_page.set_max_price(price)


@when("apply search by price")
def apply_price_search(search_page):
    search_page.submit_price()


@when(parsers.parse("select category {category}"))
def apply_filter_by_category(search_page, context, category):
    context.search_category = category
    search_page.set_category(category).search_results_grid.wait_for_grid_loaded()

@then("search results page contains correct amount of items")
def validate_amount_of_items(search_page, api, context):
    if context.search_category:
        api_result, _ = api.SearchModule.search_in_category(**context.as_dict()).quantities.goods_quantity_found
    else:
        api_result, _ = api.SearchModule.search(**context.as_dict()).quantities.goods_quantity_found

    ui_amount = search_page.get_total_amount_of_goods().split(" ")[-2]
    assert_that(int(api_result), f"Amounts doesn't match - {api_result} returned "
                                 f"from api and {ui_amount} returned from ui"
                ).is_equal_to(int(ui_amount))


@then("check item price with discount is correct")
def check_price_with_discount(search_page, api, context):
    item_with_discount = get_items_with_discount(api, context.as_dict())[0]
    ui_result = search_page.search_results_grid.get_item_by_title(item_with_discount.title)
    strategy_context = ValidationContext(DiscountValidationStrategy())
    strategy_context.validate_price(item_with_discount, ui_result)


@then("check item price without discount is correct")
def check_price_without_discount(search_page, api, context):
    item_without_discount = get_items_without_discount(api, context.as_dict())[0]
    ui_result = search_page.search_results_grid.get_item_by_title(item_without_discount.title)
    strategy_context = ValidationContext(PriceValidationStrategy())
    strategy_context.validate_price(item_without_discount, ui_result)


@scenario("test_search_ui_with_factory.feature", "Search by text")
def test_check_ui_search(ui_page):
    pass


@scenario("test_search_ui_with_factory.feature", "Search by existing item and check correct result returned")
def test_check_ui_search_by_one_item(ui_page):
    pass


@scenario("test_search_ui_with_factory.feature", "Search by producer and check correct result returned")
def test_check_ui_search_by_producer(ui_page):
    pass


@scenario("test_search_ui_with_factory.feature", "Search by multiple producers and check filter functionality")
def test_check_ui_search_by_multiple_producers_filter(ui_page):
    pass


@scenario("test_search_ui_with_factory.feature", "Search by price range and category")
def test_check_ui_search_by_price_and_cat_filter(ui_page):
    pass


@scenario("test_search_ui_with_factory.feature", "Validate price")
def test_validate_price(ui_page):
    pass

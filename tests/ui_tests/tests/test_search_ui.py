from assertpy import assert_that
from pytest_bdd import when, then, parsers, scenario

from helpers.api_helpers import get_items_with_discount, get_items_without_discount
from tests.ui_tests.common_steps.validation_strategy import ValidationContext, DiscountValidationStrategy, \
    PriceValidationStrategy


@when(parsers.parse('enter text {text} into search field'))
def enter_text_into_search_input(ui_app, text, context):
    context.text = text
    ui_app.common_steps.search_steps.send_text_to_search_input(text)


@then("click search button")
@when("click search button")
def click_search_button(ui_app):
    ui_app.common_steps.search_steps.click_search_button()
    ui_app.pages.search_results_page.search_results_grid.wait_for_grid_loaded()


@then("search results page contains correct header")
def check_search_results_header(ui_app, context):
    ui_app.common_steps.search_steps.validate_header_text(context.text)


@then(parsers.parse("filter {filter_item} is selected in filter panel"))
def verify_producer_is_selected_in_filter(ui_app, filter_item):
    ui_app.pages.search_results_page.search_results_grid.wait_for_grid_loaded()
    assert_that(ui_app.pages.search_results_page.search_results_grid.is_checkbox_selected(filter_item)).is_true()


@when(parsers.parse("select filters {filters} in filter panel"))
def select_filter_item_in_filter(ui_app, context, filters):
    context.filters_list = filters.replace(" ", "").split(",")
    for filter_item in context.filters_list:
        ui_app.pages.search_results_page.search_results_grid.filter_by_checkbox(filter_item)


@when(parsers.parse("select producers {filters} in filter panel"))
def select_producer_item_in_filter(ui_app, context, filters):
    context.filters_list = filters.replace(" ", "").split(",")
    for filter_item in context.filters_list:
        if not ui_app.pages.search_results_page.search_results_grid.is_checkbox_selected(filter_item):
            ui_app.pages.search_results_page.set_producer(filter_item)


@when(parsers.parse("set min price in filter panel to {price}"))
def set_min_price_in_filter(ui_app, context, price):
    context["min_price"] = price
    ui_app.pages.search_results_page.set_min_price(price)


@when(parsers.parse("set max price in filter panel to {price}"))
def set_max_price_in_filter(ui_app, context, price):
    context["max_price"] = price
    ui_app.pages.search_results_page.set_max_price(price)


@when("apply search by price")
def apply_price_search(ui_app):
    ui_app.pages.search_results_page.submit_price()


@when(parsers.parse("select category {category}"))
def apply_filter_by_category(ui_app, context, category):
    context.category = category
    ui_app.pages.search_results_page.set_category(category)


@then("search results page contains correct amount of items")
def validate_amount_of_items(ui_app, api, context):
    if "category" in context:
        api_result = api.SearchModule.search_in_category(**context.as_dict())[0].quantities.goods_quantity_found
    else:
        api_result = api.SearchModule.search(**context.as_dict()).quantities.goods_quantity_found

    ui_amount = ui_app.common_steps.search_steps.get_total_amount_of_goods().split(" ")[-2]
    assert_that(int(api_result), f"Amounts doesn't match - {api_result} returned "
                                 f"from api and {ui_amount} returned from ui"
                ).is_equal_to(int(ui_amount))


@then("check item price with discount is correct")
def check_price_with_discount(ui_app, api, context):
    item_with_discount = get_items_with_discount(api, context.as_dict())[0]
    ui_result = ui_app.pages.search_results_page.search_results_grid.get_item_by_title(item_with_discount.title)
    strategy_context = ValidationContext(DiscountValidationStrategy())
    strategy_context.validate_price(item_with_discount, ui_result)


@then("check item price without discount is correct")
def check_price_without_discount(ui_app, api, context):
    item_without_discount = get_items_without_discount(api, context.as_dict())[0]
    ui_result = ui_app.pages.search_results_page.search_results_grid.get_item_by_title(item_without_discount.title)
    strategy_context = ValidationContext(PriceValidationStrategy())
    strategy_context.validate_price(item_without_discount, ui_result)


@scenario("test_search_ui.feature", "Search by text")
def test_check_ui_search(ui_app):
    pass


@scenario("test_search_ui.feature", "Search by existing item and check correct result returned")
def test_check_ui_search_by_one_item(ui_app):
    pass


@scenario("test_search_ui.feature", "Search by producer and check correct result returned")
def test_check_ui_search_by_producer(ui_app):
    pass


@scenario("test_search_ui.feature", "Search by multiple producers and check filter functionality")
def test_check_ui_search_by_multiple_producers_filter(ui_app):
    pass


@scenario("test_search_ui.feature", "Search by price range and category")
def test_check_ui_search_by_price_and_cat_filter(ui_app):
    pass


@scenario("test_search_ui.feature", "Validate price")
def test_validate_price(ui_app):
    pass

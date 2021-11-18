from assertpy import assert_that
from pytest_bdd import scenario, when, then, parsers


@when(parsers.parse("Searching by text {text}"))
def search_by_text(api, text, context):
    context.response = api.SearchModule.search(text=text)


@then(parsers.parse("response code is {code}"))
def check_response_code(context, code):
    assert_that(context.response.status_code).is_equal_to(200)


@then(parsers.parse("amount of found items is {amount}"))
def check_amount_of_items_is_correct(context, amount):
    found_goods = context.response.quantities.goods_quantity_found
    assert_that(found_goods, f"Wrong goods amount: {found_goods} instead of {amount}").is_equal_to(int(amount))


@when(parsers.parse("search by text {text} in category {category}"))
def search_in_category(api, context, text, category):
    params = {"category": category, "text": text}
    context.response, context.cat_id = api.SearchModule.search_in_category(**params)


@then(parsers.parse("all items have category {category}"))
def check_results_have_correct_category(api, context, category):
    wrong_category_items = [item.category_id for item in context.response.goods if item.category_id != context.cat_id]
    assert_that(len(wrong_category_items), f"expected - all items with category id ${category}"
                                           f"but found items with different category").is_equal_to(0)


@scenario("search_tests.feature", "Search by text and verify response code is correct")
def test_search_by_text():
    pass


@scenario("search_tests.feature", "Search by text and verify correct items returned")
def test_check_returned_items():
    pass

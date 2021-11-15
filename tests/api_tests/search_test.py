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


@scenario("search_tests.feature", "Search by text and verify response code is correct")
def test_search_by_text():
    pass


@scenario("search_tests.feature", "Search by text and verify correct items returned")
def test_check_returned_items():
    pass

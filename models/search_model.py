from typing import List, Any

from lib.api.response_model import ResponseModel


class QuantityModel:
    goods_quantity_max: int
    goods_quantity_found: int
    goods_quantity_total_found: int

    def __init__(self, resp):
        self.goods_quantity_max = resp["goods_quantity_max"]
        self.goods_quantity_found = resp["goods_quantity_found"]
        self.goods_quantity_total_found = resp["goods_quantity_total_found"]


class GoodsModel:
    id: str
    title: str
    category_id: str
    old_price: float = None
    price: float = None
    status: str
    brand_id: str
    producer_id: str

    def __init__(self, resp):
        self.id = resp["id"]
        self.title = resp["title"]
        self.category_id = resp["category_id"]
        self.price = float(resp["price"])
        self.status = resp["status"]
        self.brand_id = resp["brand_id"]
        self.producer_id = resp["producer_id"]
        self.old_price = float(resp["old_price"])


class SubCategories:

    def __init__(self, resp):
        self.children = [SubCategories(item) for item in resp["children"]]
        self.id = resp["id"]
        self.count = resp["count"]
        self.title = resp["title"]


class Categories:
    goods_quantity: int
    list_categories: List[SubCategories]
    option_name: str
    option_title: str

    def __init__(self, resp):
        self.goods_quantity = resp["goods_quantity"]
        self.list_categories = [SubCategories(item) for item in resp["list_categories"]]
        self.option_name = resp["option_name"]
        self.option_title = resp["option_title"]


class SearchResponseModel(ResponseModel):
    status_code: int
    errors: Any
    quantities: QuantityModel
    goods: List[GoodsModel]
    categories: Categories

    def __init__(self, resp: ResponseModel):
        self.status_code = resp.status_code
        self.errors = resp.error
        self.goods = [GoodsModel(item) for item in resp.data['goods']]
        self.quantities = QuantityModel(resp.data['quantities'])
        self.categories = Categories(resp.data['categories'])

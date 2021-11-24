from typing import Any

from lib.api.response_model import ResponseModel


class GoodsItemModel(ResponseModel):
    status_code: int
    errors: Any
    old_price: int
    old_price_formatted: str
    old_usd_price: str
    price: float
    price_formatted: str
    sell_status: str
    status: str
    usd_price: str

    def __init__(self, resp: ResponseModel):
        self.status_code = resp.status_code
        self.errors = resp.error
        self.old_price = resp.payload['old_price']
        self.old_price_formatted = resp.payload['old_price_formatted']
        self.old_usd_price = resp.payload['old_usd_price']
        self.price = resp.payload['price']
        self.price_formatted = resp.payload['price_formatted']
        self.sell_status = resp.payload['sell_status']
        self.status = resp.payload['status']
        self.usd_price = resp.payload['usd_price']

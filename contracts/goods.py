from requests import Session

from models.goods_item_model import GoodsItemModel


class ApiGoods:
    def __init__(self, api):
        self.goods_path = "/v2/goods/get-price"
        self.api: Session = api
        self.search_params = {}

    def get_goods_item_by_id(self, id, **kwargs):
        """
        search by parameters
        :param kwargs: content will be added to query params
        :return: GoodsItemModel
        """
        self.search_params.update({"id": id})
        self.search_params.update(kwargs)
        resp = self.api.get(f"{self.goods_path}/", params=self.search_params)
        return GoodsItemModel(resp)
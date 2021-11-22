from contracts.goods import ApiGoods
from contracts.search import ApiSearch


class APIFacade:
    def __init__(self, api):
        self.SearchModule = ApiSearch(api.api)
        self.GetGoodsItemModule = ApiGoods(api.common_api)

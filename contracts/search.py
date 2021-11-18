from requests import Session

from helpers.api_helpers import get_category_id_by_title
from models.search_model import SearchResponseModel


class ApiSearch:

    def __init__(self, api):
        self.search_path = "/search/api/v6"
        self.api: Session = api
        self.search_params = {"front-type": "xl", "lang": "ru"}

    def search(self, **kwargs):
        self.search_params.update(kwargs)
        resp = self.api.get(f"{self.search_path}/", params=self.search_params)
        return SearchResponseModel(resp)

    def search_in_category(self, **kwargs):
        try:
            cat = kwargs.pop("category")
            cat_id = get_category_id_by_title(self.search(**kwargs), cat)
            kwargs["section_id"] = cat_id
        except KeyError:
            raise ValueError("No such category in the list")
        self.search_params.update(kwargs)
        resp = self.api.get(f"{self.search_path}/", params=self.search_params)
        return SearchResponseModel(resp), cat_id

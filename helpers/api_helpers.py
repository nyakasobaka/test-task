from models.search_model import SearchResponseModel


def get_items_with_discount(client, params: dict):
    resp, _ = client.SearchModule.search_in_category(**params)
    return [item for item in resp.goods if item.old_price and item.old_price > item.price]


def get_items_without_discount(client, params: dict):
    resp, _ = client.SearchModule.search_in_category(**params)
    return [item for item in resp.goods if item.price > 0 and item.old_price <= item.price]


def get_category_id_by_title(resp: SearchResponseModel, category_title: str):
    subcategories = [category.children for category in resp.categories.list_categories]
    section_id = [child_cat.id for category in subcategories for child_cat in category if
                  child_cat.title == category_title]
    if len(section_id) > 0:
        return section_id[0]
    else:
        raise ValueError("No such category")


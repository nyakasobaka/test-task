from contracts.search import ApiSearch


class APIFacade:
    def __init__(self, api):
        self.SearchModule = ApiSearch(api)

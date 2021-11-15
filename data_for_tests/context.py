class Context:
    def __init__(self, initial_data: dict = None):
        if initial_data:
            self.__dict__.update(initial_data)

    def __getitem__(self, key):
        key = self._prepare_key(key)
        return self.__dict__[key]

    def __setitem__(self, key, value):
        key = self._prepare_key(key)
        self.__dict__[key] = value

    def __delitem__(self, key):
        key = self._prepare_key(key)
        del self.__dict__[key]

    def __contains__(self, key):
        key = self._prepare_key(key)
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def as_dict(self):
        return self.__dict__


    @staticmethod
    def _prepare_key(key: str):
        return key.replace(" ", "_").lower()



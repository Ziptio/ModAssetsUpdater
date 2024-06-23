from abc import abstractmethod


class Platform:

    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get_mod_body(self, mod_body: dict[str, str]):
        pass

    @abstractmethod
    def set_mod_body(self, mod_body: dict[str, str]):
        pass

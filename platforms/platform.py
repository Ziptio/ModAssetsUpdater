from abc import abstractmethod


class Platform:

    def __init__(self, platform_id, auth_token):
        self.id = platform_id
        self.auth_token = auth_token

    @abstractmethod
    def get_mod_body(self, mod_body: dict[str, str]):
        pass

    @abstractmethod
    def set_mod_body(self, mod_body: dict[str, str], auth_token: str):
        pass

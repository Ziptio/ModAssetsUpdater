from platforms.platform import Platform

curseforge_api = ""

# TODO: Needs to be implemented.
#  I'm actually not even sure if Curseforge allows you to modify anything through their API


class Curseforge(Platform):

    def __init__(self, label):
        super().__init__(label)

    def get_mod_body(self, mod_body: dict[str, str]):
        pass

    def set_mod_body(self, mod_body: dict[str, str]):
        pass

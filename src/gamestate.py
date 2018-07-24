from .custom_driver import client


class slot:
    def __init__(self, browser: client, id: int):
        self.browser = browser
        self.id = id
        self.upgradable = False
        self.field = id < 19
        self.lvl = -1


class village:
    def __init__(self, browser: client, name: str, index: int):
        self.slots = []
        self.browser = browser

        self.upgradeList = []

        self.name = name
        self.index = index
# 1-18 = ress
# 19-40 = city


class gameworld:
    def __init__(self, browser: client, world: str):
        self.world = world.lower()
        self.browser = browser

        # init
        self.villages = []
        self.delayCheckAdventures = 60

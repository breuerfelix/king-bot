class slot:
    def __init__(self, id: int):
        self.id = id
        self.upgradable = False
        self.field = id < 19
        self.lvl = -1


class village:
    def __init__(self, name: str, index: int):
        self.slots = []

        self.name = name
        self.index = index
# 1-18 = ress
# 19-40 = city


class gameworld:
    def __init__(self, world: str):
        self.world = world.lower()

        # init
        self.villages = []

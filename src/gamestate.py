from .custom_driver import client
from .slot import find_slot
from .utils import log
from util_game import close_modal


def load_slot_data(browser: client, id: int) -> dict:
    el = find_slot(browser, id)
    templvl = el.find_element_by_class_name("buildingLevel")
    lvl = templvl.get_attribute("innerHTML")
    temp_upgrade = el.find_element_by_xpath(
        ".//div[contains(@class, 'colorLayer')]").get_attribute("class")

    if "possible" in temp_upgrade:
        upgradable = True

    return {'lvl': lvl, 'upgradeable': upgradable}


def init_villages(browser: client) -> list:
    villages:list  = []

    btn = browser.find("//a[@id='villageOverview']")
    browser.click(btn, 1)

    table = browser.find(
        "//table[contains(@class, 'villagesTable')]/tbody")
    villages = table.find_elements_by_xpath(".//tr")

    for vil in villages:
        tds = vil.find_elements_by_xpath(".//td")

        name = tds[0].find_element_by_xpath(
            ".//a").get_attribute("innerHTML")

        # villages.append(
        #   village(browser, name, villages.index(vil)))
        #log("village {} added".format(name))

    close_modal(browser)
    return villages


def checkBuildingSlot(browser: client):
    slots = browser.driver.find_elements_by_xpath(
        "//div[@class='masterBuilderContainer']/div[contains(@class, 'buildingQueueSlot')]")

    freeSlots = 0
    locked = False

    for slot in slots:
        if locked:
            break

        classes = slot.get_attribute("class").split(" ")
        for c in classes:
            if "empty" == c:
                freeSlots += 1

            if "locked" == c:
                locked = True
                break

    return freeSlots


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

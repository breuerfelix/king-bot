from .custom_driver import client, use_browser
from .slot import find_slot
from .utils import log
import time
from random import randint
from .village import open_building, open_village, open_city


def upgrade_slot(browser: client, id: int) -> None:
    el = find_slot(browser, id)
    el = el.find_element_by_xpath(".//div[contains(@class, 'clickable')]")
    browser.click(el, 1)
    browser.click(el, 1)

    log("added slot: {} to queue".format(id))


def upgrade_units_smithy_thread(browser: client, village: int, units: list, interval: int) -> None:
    time.sleep(randint(0, 10))

    while True:
        sleep_time: int = interval

        upgrade_units_smithy(browser, village, units)

        time.sleep(sleep_time)


@use_browser
def upgrade_units_smithy(browser: client, village: int, units: list):
    open_village(browser, village)
    pass

from .custom_driver import client, use_browser
from .slot import find_slot
from .utils import log
from .util_game import close_modal
import time
from random import randint
from .village import open_building, open_village, open_city, open_building_type, building
from datetime import timedelta

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

        rv = upgrade_units_smithy(browser, village, units)
        #log("upgrade units in smithy thread going to sleep ...")

        if rv != -1:
            if rv is None:
                log("smithy is busy.")
            else:
                sleep_time = rv
                log("smithy is busy. going to sleep for " + 
                    "{:0>8}".format(str(timedelta(seconds=sleep_time))) + ".")

        time.sleep(sleep_time)


@use_browser
def upgrade_units_smithy(browser: client, village: int, units: list) -> int:
    #log("upgrade units in smithy thread waking up ...")

    open_village(browser, village)
    open_city(browser)
    open_building_type(browser, building.smithy)

    smith = browser.find("//div[contains(@class, 'blacksmith')]")
    carousel = smith.find_element_by_xpath(".//div[@class='carousel']")
    pages = carousel.find_element_by_xpath(".//div[contains(@class, 'pages')]")
    classes = pages.get_attribute("class")

    # todo implement pages
    pages = "ng-hide" not in classes  # true if there are more than one page

    item_container = carousel.find_element_by_xpath(".//div[@class='items']")
    items = item_container.find_elements_by_xpath("./*")

    countdown = ""
    available_units: dict = {}

    for item in items:
        unit = item.find_element_by_xpath(".//div[contains(@class, 'unit')]")
        classes = unit.get_attribute("class")

        if "ng-hide" not in classes:
            # continue because no dummy container

            # get unit id
            unit_img = unit.find_element_by_xpath(
                ".//img[contains(@class, 'itemImage')]")
            unit_id = int(unit_img.get_attribute("data"))

            item_body = unit.find_element_by_xpath(".//div[@class='itemBody']")

            # check for progress bar
            progress_container = item_body.find_element_by_xpath(
                ".//div[contains(@class, 'progressContainer')]")
            classes = progress_container.get_attribute("class")

            if "ng-hide" not in classes:
                # here is a loading bar
                countdown_div = progress_container.find_element_by_xpath(
                    ".//div[@class='countdown']")
                countdown = countdown_div.get_attribute("innerHTML")

            # check if unit is locked
            divs = item_body.find_elements_by_xpath("./*")
            locked = False
            for div in divs:
                classes = div.get_attribute("class")
                if "lockExplain" in classes:
                    locked = True

            if not locked:
                # add to dict
                available_units[unit_id] = unit_img

    if countdown:
        cd_list = countdown.split(":")
        cd = int(cd_list[0]) * 60 * 60 + int(cd_list[1]) * 60 + int(cd_list[2])
        close_modal(browser)
        log("upgrade postponed for " + cd_list[0] + " hours " + cd_list[1] + " minutes " + cd_list[2] + " seconds.")
        return cd
    else:
        for un in units:
            if un in available_units:
                browser.click(available_units[un], 1)
                log("will try to upgrade unit: " + str(un) + " in village: " + str(village) + ".")
                break

        # click upgrade button
        improve = browser.find("//button[contains(@clickable, 'research')]")
        classes = improve.get_attribute("class").split(" ")
        available = True

        for c in classes:
            if c == "disabled":
                available = False
                break

        if available:
            browser.click(improve, 1)
            log("upgrade started.")

        close_modal(browser)
        return -1

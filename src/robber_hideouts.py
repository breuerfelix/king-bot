from .custom_driver import client, use_browser
from .utils import log
from .util_game import close_modal
import time
from .village import open_village, open_city, open_map


def robber_hideout_thread(
    browser: client, village: int, units: dict, interval: int
) -> None:
    while True:
        robber = check_robber(browser, village)
        if robber:
            outgoing_troops = check_troops(browser)
            if outgoing_troops:
                log("troops are busy right now.")
            else:
                send_troops(browser, village, robber, units)
        else:
            log("there is no Robber Hideout right now, will check again later.")

        time.sleep(interval)


@use_browser
def send_troops(browser: client, village: int, robber, units: dict) -> None:
    if robber is None:
        log("parsing webelement failed")
        return
    open_village(browser, village)
    open_map(browser)
    browser.hover(robber)
    browser.hover(robber)

    robber_name = robber.text
    browser.click(robber, 2)

    item_pos1 = browser.find("//div[contains(@class, 'item pos1')]")
    browser.click(item_pos1, 2)

    raid_button = browser.find(
        "//div[contains(@class, 'clickableContainer missionType4')]"
    )
    browser.click(raid_button, 2)

    input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
    input = input.find_elements_by_xpath(".//td")

    units_sent = False
    units_total = 0

    if -1 in units:
        # send all units, max count
        for inp in input:
            inp = inp.find_element_by_xpath(".//input")
            dis = inp.get_attribute("disabled")
            if not dis:
                inp.click()
                number = inp.get_attribute("number")
                inp.send_keys(number)
                units_sent = True
    else:
        # send value amount of units with index key
        for key, value in units.items():
            inp = input[int(key)].find_element_by_xpath(".//input")
            # check if the field is disabled
            dis = inp.get_attribute("disabled")

            if not dis:
                # gets max available troop count
                number = inp.get_attribute("number")

                units_to_send = int(value)

                # send all units if value is -1
                if units_to_send == -1:
                    units_to_send = int(number)
                else:
                    if int(number) < units_to_send:
                        # send max value if there arent enough units to send
                        units_to_send = number

                inp.click()
                inp.send_keys(units_to_send)
                units_sent = True
                units_total += units_to_send

    if not units_sent:
        log("no units available to sent.")
        close_modal(browser)
        open_city(browser)
        return

    time.sleep(1)
    send_button_1 = browser.find("//button[contains(@class, 'next clickable')]")
    browser.click(send_button_1, 2)

    send_button_2 = browser.find("//button[contains(@class, 'sendTroops clickable')]")
    browser.click(send_button_2, 2)

    log("sent " + str(units_total) + " units to " + robber_name + ".")
    open_city(browser)


@use_browser
def check_troops(browser: client) -> bool:
    movements = browser.find("//div[@id='troopMovements']")
    ul = movements.find_element_by_xpath(".//ul")
    lis = ul.find_elements_by_xpath(".//li")

    for li in lis:
        classes = li.get_attribute("class")
        if "outgoing_attacks" in classes:
            return True
        elif "return" in classes:
            return True

    open_city(browser)
    return False


@use_browser
def check_robber(browser: client, village: int):
    open_village(browser, village)
    map_button = browser.find("//a[contains(@class, 'navi_map bubbleButton')]")
    browser.click(map_button, 1)
    overlay_markers = browser.find("//div[@id='overlayMarkers']")
    divs = overlay_markers.find_elements_by_xpath(".//div")
    for listed in divs:
        attribute = listed.get_attribute("class")
        if "robber" in attribute:
            span = listed.find_element_by_xpath(".//span")
            span_attribute = span.get_attribute("class")
            if "jsVillageType5" in span_attribute:
                browser.hover(span)
                browser.hover(span)
                return span

    open_city(browser)
    return None

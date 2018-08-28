from .custom_driver import client, use_browser
from .utils import log
from .util_game import close_modal
import time
from .village import open_city

def robber_hideout_thread(browser: client, interval: int) -> None:
    while True:
        robber = check_robber(browser)
        if robber:
            outgoing_troops = check_troops(browser)
            if outgoing_troops:
                open_city(browser)
                log("Troops is busy right now.")
            else:
                send_troops(browser, robber)
                open_city(browser)
                log("Troops sent.")
        else:
            open_city(browser)
            log("There is no Robber Hideout right now, will check again later.")

        time.sleep(interval)
        log("Refreshing the page.")
        browser.refresh()
        time.sleep(25)

@use_browser
def send_troops(browser: client, robber) -> None:
    if robber is None:
        log("Parsing webelement failed")
        return
    browser.click(robber, 2)

    item_pos1 = browser.find("//div[contains(@class, 'item pos1')]")
    browser.click(item_pos1, 2)

    raid_button = browser.find("//div[contains(@class, 'clickableContainer missionType4')]")
    browser.click(raid_button, 2)

    input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
    input = input.find_elements_by_xpath(".//td")
    for inp in input:
        inp = inp.find_element_by_xpath(".//input")
        dis = inp.get_attribute("disabled")
        if not dis:
            number = inp.get_attribute("number")
            inp.send_keys(number)
            time.sleep(1)

    time.sleep(1)
    send_button_1 = browser.find("//button[contains(@class, 'next clickable')]")
    browser.click(send_button_1, 2)

    send_button_2 = browser.find("//button[contains(@class, 'sendTroops clickable')]")
    browser.click(send_button_2, 2)

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

    return False

@use_browser
def check_robber(browser: client):
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

    return None

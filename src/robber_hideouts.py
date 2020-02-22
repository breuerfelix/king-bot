from .custom_driver import client, use_browser
from .utils import log
from .util_game import close_modal
import time
from .village import open_village, open_city
from .worker import worker

def robber_hideout_thread(thread: worker, browser: client, village: int, interval: int, units: list) -> None:
    while True:
        thread.wait()
        thread.pause()
        open_village(browser, village)
        robber = check_robber(browser)
        if robber:
            robber_name = robber.text
            outgoing_troops = check_troops(browser)
            if outgoing_troops:
                open_city(browser)
                log("troops are busy right now.")
            else:
                # send units
                unit_dict = {}
                # fill the dict, -1 means send all units
                for unit in units:
                    unit_dict[int(unit)] = -1
                send_troops(browser, robber, unit_dict)
                open_city(browser)
                log("troops sent to " + robber_name + ".")
        else:
            open_city(browser)
            log("there is no Robber Hideout right now, will check again later.")
        
        thread.resume()
        time.sleep(interval)
        #log("Refreshing the page.")
        #browser.refresh()
        #time.sleep(25)

@use_browser
def send_troops(browser: client, robber, units: dict) -> None:
    if robber is None:
        log("parsing webelement failed")
        return
    browser.click(robber, 2)

    item_pos1 = browser.find("//div[contains(@class, 'item pos1')]")
    browser.click(item_pos1, 2)

    raid_button = browser.find("//div[contains(@class, 'clickableContainer missionType4')]")
    browser.click(raid_button, 2)

    input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
    input = input.find_elements_by_xpath(".//td")

    units_sent = False

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

    if not units_sent:
        log("no units available to sent.")
        close_modal(browser)
        return

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

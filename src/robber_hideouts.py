from .custom_driver import client, use_browser
from threading import Thread
from .utils import log
from .util_game import close_modal
import time
from .farming import send_farm

def robber_hideout_thread(browser: client, interval: int):
    threshold = [1, 0]
    while True:
        robber = check_robber(browser)
        current_troops = check_troops(browser)
        if robber:
            if robber[1] is True:
                pass
            else:
                if sum(current_troops) < sum(threshold):
                    pass
                else:
                    unit_dict = {0: 110, 1: 110, 10: 99}
                    send_farm(browser=browser, village=0, units=unit_dict, x=robber[2], y=robber[3])

        #log(current_troops)
        #log(robber)
        time.sleep(interval)

@use_browser
def check_troops(browser: client) -> list:
    units = ["unitType1", "unitType2"]
    current_troops = []
    int_current_troops = []
    foo = 0
    troops_stationed = browser.find("//div[@id='troopsStationed']")
    ul = troops_stationed.find_element_by_xpath(".//ul[@class='troopsStationed']")
    uls = ul.find_elements_by_xpath(".//ul")
    li = uls[0].find_elements_by_xpath(".//li")
    for listed in li[1:]:
        iis = listed.find_element_by_xpath(".//i")
        divs = listed.find_element_by_xpath(".//div")
        iis_class = iis.get_attribute("class").split(" ")
        divs_count = divs.get_attribute("innerHTML")
        for unit in units:
            if unit in iis_class:
                current_troops.append(divs_count)

    for current_troops_unit in current_troops:
        int_current_troops.append(int(current_troops_unit))
    return int_current_troops

@use_browser
def check_robber(browser: client) -> list:
    robber_info = []
    map_button = browser.find("//a[contains(@class, 'navi_map bubbleButton')]")
    browser.click(map_button, 1)
    overlay_markers = browser.find("//div[@id='overlayMarkers']")
    try:
        overlay_markers = overlay_markers.find_element_by_xpath(".//div[@class='villageName unselectable robber']")
        robber_element = overlay_markers.find_element_by_xpath(".//span")
        span_attribute = robber_element.get_attribute("class").split(" ")
        if "jsVillageType5" in span_attribute:
            robber_name = robber_element.get_attribute("innerHTML")
            #log(robber_name)
            browser.hover(robber_element, 1)
            browser.hover(robber_element, 1)
            #log("It should've hovering to Robber right?")
            #time.sleep(3)
            info_movements = browser.find("//div[contains(@class, 'infoMovements unselectable')]")
            ul = info_movements.find_element_by_xpath(".//ul[@class='troopMovements']")
            try:
                li = ul.find_element_by_xpath(".//li[contains(@class, 'incoming_attacks')]")
                tile_information = browser.find("//div[@id='tileInformation']")
                tile_information = tile_information.find_element_by_xpath(".//span[@class='coordinateWrapper']")
                x_coordinate = int(tile_information.get_attribute("x"))
                y_coordinate = int(tile_information.get_attribute("y"))
                robber_info.append(robber_name)
                robber_info.append(True)
                robber_info.append(x_coordinate)
                robber_info.append(y_coordinate)
                #log("{0} is Under Attacks".format(robber_name))
                return robber_info
                #return list contains Robber data. The data is 'Boolean Under Attacks, x coordinate, y coordinate'
            except:
                tile_information = browser.find("//div[@id='tileInformation']")
                tile_information = tile_information.find_element_by_xpath(".//span[@class='coordinateWrapper']")
                x_coordinate = int(tile_information.get_attribute("x"))
                y_coordinate = int(tile_information.get_attribute("y"))
                robber_info.append(robber_name)
                robber_info.append(False)
                robber_info.append(x_coordinate)
                robber_info.append(y_coordinate)
                #log("There is no Attacks to {0}".format(robber_name))
                return robber_info
                #return list contains Robber data. The data is 'Boolean Under Attacks, x coordinate, y coordinate'
        else:
            #log("There is no Robber Hideout. \nPS: Robber Camp different with Robber Hideout.")
            return robber_info
            #return empty list
    except:
        #log("There is no Robber Hideout")
        return robber_info
        #return empty list

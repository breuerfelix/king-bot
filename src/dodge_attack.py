from .custom_driver import client, use_browser
import time
from random import randint
from .utils import log
from .village import open_village, open_city, open_building
from .farming import send_farm
from .util_game import close_modal, shortcut, check_resources


def check_for_attack_thread(browser: client, village: int, interval: int, units: list, target: list) -> None:
    time.sleep(randint(0, 10))

    while True:
        sleep_time = interval
        attack_time = check_for_attack(browser, village)

        if attack_time:
            timelist = attack_time.split(":")
            countdown = int(timelist[0]) * 60 * 60 + \
                int(timelist[1]) * 60 + int(timelist[0])
            save_send_time = 10 * 60

            if countdown < save_send_time:
                # send units away
                unit_dict = {}
                # fill the dict, -1 means send all units
                for unit in units:
                    unit_dict[int(unit)] = -1

                send_farm(browser=browser, village=village,
                          units=unit_dict, x=int(target[0]), y=int(target[1]))

                log("units sent to rescue")
                save_resources(browser, [1000, 1000, 1000, 2000])

                sleep_time = save_send_time  # sleep at least until attack is over
            elif countdown > sleep_time + save_send_time:
                # do nothing and wait for next waking up
                pass
            else:
                # wake up before attack so the countdown will be smaller than save_send_time
                sleep_time = countdown - (save_send_time - 10)
            pass

        #log("checking for attacks going to sleep")
        time.sleep(sleep_time)


@use_browser
def check_for_attack(browser: client, village: int) -> str:
    #log("checking for incoming attacks...")

    open_village(browser, village)

    movements = browser.find("//div[@id='troopMovements']")
    ul = movements.find_element_by_xpath(".//ul")
    lis = ul.find_elements_by_xpath(".//li")

    for li in lis:
        classes = li.get_attribute("class")
        if "incoming_attacks" in classes:
            cd = li.find_element_by_xpath(".//div[@class='countdown']")
            countdown = cd.get_attribute("innerHTML")

            log("incoming attack in {} !".format(countdown))

            return countdown

    return ""

@use_browser
def save_resources(browser: client, threshold: list):
    shortcut(browser, "barrack")
    el = browser.find("//div[@class='modalContent']")
    max_button = el.find_element_by_xpath(".//div[@class='iconButton maxButton clickable']")
    browser.click(max_button, 1)
    time.sleep(1)
    train_button = browser.find("//button[contains(@class, 'animate footerButton')]")
    browser.click(train_button, 1)
    close_modal(browser)
    #put resource left to market based on threshold
    resource = check_resources(browser)
    foo = 0
    shortcut(browser, "marketplace")
    el = browser.find("//div[@class='modalContent']")
    sell_tab = el.find_element_by_xpath(".//a[contains(@class, 'naviTabSell clickable')]")
    browser.click(sell_tab, 1)
    merchant = el.find_element_by_xpath(".//div[@class='marketplaceHeaderGroup']")
    merchant = merchant.find_element_by_xpath(".//div[@class='circle']/span")
    merchant = int(merchant.get_attribute("innerHTML"))
    time.sleep(1)
    if merchant > 0:
        for res_name in resource.keys():
            if resource[res_name] >= threshold[foo]:
                offering = browser.find("//div[@class='offerBox']")
                offering = offering.find_element_by_xpath(".//div[@class='resourceFilter filterBar']")
                offering_type = offering.find_elements_by_xpath(".//a[contains(@class, 'filter iconButton')]")
                browser.click(offering_type[foo], 1)
                input_offering = browser.find("//input[@id='marketNewOfferOfferedAmount']").send_keys("1000")
                searching = browser.find("//div[@class='searchBox']")
                searching = searching.find_element_by_xpath(".//div[@class='resourceFilter filterBar']")
                searching_type = searching.find_elements_by_xpath(".//a[contains(@class, 'filter iconButton')]")
                browser.click(searching_type[(foo+1)%2], 1)
                input_searching = browser.find("//input[@id='marketNewOfferSearchedAmount']").send_keys("2000")
                time.sleep(1)
                while resource[res_name] >= threshold[foo] and merchant > 0:
                    sell_btn = browser.find("//button[contains(@class, 'createOfferBtn')]")
                    browser.click(sell_btn, 1)
                    resource[res_name] -= 1000
                    merchant -= 1
            time.sleep(1)
            foo += 1
    time.sleep(1)
    close_modal(browser)

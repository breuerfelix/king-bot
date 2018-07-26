from .custom_driver import client, use_browser
import time
from random import randint
from .utils import log
from .village import open_village, open_city, open_building


def check_for_attack_thread(browser: client, village: int, interval: int, units: list, target: list):
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
                save_units(browser, village, units, target)
                sleep_time = save_send_time  # sleep at least until attack is over
            elif countdown > sleep_time + save_send_time:
                # do nothing and wait for next waking up
                pass
            else:
                # wake up before attack so the countdown will be smaller than save_send_time
                sleep_time = countdown - sleep_time - 10
            pass

        log("checking for attacks going to sleep")
        time.sleep(sleep_time)


@use_browser
def check_for_attack(browser: client, village: int) -> str:
    log("checking for incoming attacks...")

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

    return None


@use_browser
def save_units(browser: client, village: int, units: list, target: list):
    if units:
        if not target:
            return

    open_village(browser, village)
    open_city(browser)
    open_building(browser, 32)
    btn = browser.find("//button[contains(@class, 'sendTroops')]")
    browser.click(btn, 2)

    input = browser.find(
        "//div[@class='modalContent']")
    input = input.find_element_by_xpath(
        ".//input[contains(@class, 'targetInput')]")
    input.send_keys("({}|{})".format(target[0], target[1]))
    browser.sleep(1)

    btn = browser.find(
        "//div[contains(@class, 'clickableContainer missionType4')]")
    browser.click(btn)

    input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
    input = input.find_elements_by_xpath(".//td")

    if units[0] == -1:
        # send all units !
        for inp in input:
            inp = inp.find_element_by_xpath(".//input")
            dis = inp.get_attribute("disabled")
            if not dis:
                number = inp.get_attribute("number")
                inp.send_keys(number)
    else:
        for unit in units:
            inp = input[unit].find_element_by_xpath(".//input")
            dis = inp.get_attribute("disabled")
            if not dis:
                number = inp.get_attribute("number")
                inp.send_keys(number)

    btn = browser.find("//button[contains(@class, 'next clickable')]")
    browser.click(btn, 1)
    btn = browser.find(
        "//button[contains(@class, 'sendTroops clickable')]")
    browser.click(btn, 1)

    log("Farm sent: ({}/{}).".format(target[0], target[1]))

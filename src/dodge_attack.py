from .custom_driver import client, use_browser
import time
from random import randint
from .utils import log
from .village import open_village, open_city, open_building
from .farming import send_farm


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
                unit_dict = {}
                # fill the dict, -1 means send all units
                for unit in units:
                    unit_dict[int(unit)] = -1

                send_farm(browser=browser, village=village,
                          units=unit_dict, x=int(target[0]), y=int(target[1]))
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

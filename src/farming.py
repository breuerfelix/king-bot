from .custom_driver import client, use_browser
import time
from .utils import log
from .village import open_building, open_city, open_village
from .util_game import close_modal
import schedule


def start_farming_thread(browser: client, village: int, farmlists: list, interval: int):
    # todo exit when in beginners protection
    time.sleep(3)

    while True:
        start_farming(browser, village, farmlists)
        time.sleep(interval)


@use_browser
def start_farming(browser: client, village: int, farmlists: list):
    log("farming thread in village {} waking up".format(village))

    open_village(browser, village)
    open_city(browser)
    open_building(browser, 32)
    browser.sleep(1)

    tab = browser.find(
        "//a[contains(@class, 'tab naviTabFarmList')]")
    browser.click(tab, 1)

    table = browser.find(
        "//div[@class='farmList']")
    table = browser.find(
        ".//table[contains(@class, 'farmListsOverviewTable')]")
    lists = table.find_elements_by_xpath(
        ".//tbody")

    for i in farmlists:
        cb = lists[i].find_element_by_xpath(
            ".//input[@type='checkbox']")
        # cb.send_keys(Keys.SPACE)
        browser.click(cb)

    browser.sleep(0.5)
    btn = browser.find(
        "//button[contains(@class, 'startRaid')]")
    browser.click(btn, 1)
    log("farmlist sent")

    close_modal(browser)

    log("farming thread in village {} sleeping".format(village))


def sort_danger_farms_thread(browser: client, farmlists: list, to_list: int, red: bool, yellow: bool, interval: int):
    time.sleep(2)

    while True:
        sort_danger_farms(browser, farmlists, to_list, red, yellow)
        time.sleep(interval)
# endregion


@use_browser
def sort_danger_farms(browser: client, farmlists: list, to_list: int, red: bool, yellow: bool):
    print("sorting farms started...")

    open_city(browser)
    open_building(browser, 32)

    browser.sleep(1)
    tab = browser.find(
        "//a[contains(@class, 'tab naviTabFarmList')]")
    browser.click(tab, 1)

    table = browser.find(
        "//div[@class='farmList']")
    table = browser.find(
        ".//table[contains(@class, 'farmListsOverviewTable')]")
    lists = table.find_elements_by_xpath(
        ".//tbody")

    for i in farmlists:
        # opens farmlist
        cb = lists[i].find_element_by_xpath(
            ".//td[contains(@class, 'clickable')]")
        browser.click(cb)

        tbody = browser.find(
            "//div[@class='listDetail']")
        tbody = tbody.find_element_by_xpath(".//tbody")
        trs = tbody.find_elements_by_xpath(".//tr")
        for tr in trs:
            tds = tr.find_elements_by_xpath(".//td")
            try:
                icon = tds[6].find_element_by_xpath(".//i")
                translate = icon.get_attribute("tooltip-translate")
                if translate != "Notification_1":
                    print("found yellow or red farm")
                    movefarm = False
                    if translate == "Notification_2":
                        #farm is yellow
                        if yellow == True:
                            movefarm = True
                    elif translate == "Notification_3":
                        #farm is red
                        if red == True:
                            movefarm = True

                    if movefarm == True:
                        # move the farm
                        browser.hover(tds[1])
                        add = tds[9].find_element_by_xpath(
                            ".//div[contains(@clickable, 'farmListAdd')]")
                        browser.click(add, 1)

                        inner = browser.find(
                            "//div[@class='farmListInner']")
                        movelists = inner.find_element_by_xpath(
                            ".//div[contains(@class, 'list')]")

                        # todo test this !!
                        # move to new list
                        browser.hover(movelists[to_list])
                        browser.click(movelists[to_list])
                        browser.sleep(1)

                        # remove from current list
                        browser.hover(movelists[i])
                        browser.click(movelists[i])
                        browser.sleep(1)

                        modal = browser.find(
                            "//div[contains(@class, 'farmListAdd')]")
                        closemodal = modal.find_element_by_xpath(
                            ".//a[contains(@class, 'closeWindow')]")
                        browser.click(closemodal, 2)
            except:
                # farm never got sent
                pass

        # press back button
        btnback = browser.find(
            "//div[@class='back clickable']")
        browser.click(btnback, 1)

    close_modal(browser)
    print("sorting farms going to sleep")


def start_custom_farmlist_thread(browser: client, path: str):
    with open(path, "r") as file:
        lines = file.readlines()

    for line in lines:
        args = line.split(";")
        print(args)

        # shedule task
        schedule.every(int(args[2])).seconds.do(
            send_farm, browser=browser, x=args[0], y=args[1], village=args[3], units=args[4])
        print("job started")

    browser.use()

    for line in lines:
        args = line.split(";")
        # send one time at start
        send_farm(browser=browser, x=args[0],
                  y=args[1], village=args[3], units=args[4])

    browser.done()

    while True:
        schedule.run_pending()
        time.sleep(1)


@use_browser
def send_farm(browser: client, x: int, y: int, village: int, units: list):
    log("Sending farm: ({}/{}) ...".format(x, y))

    open_village(browser, int(village))
    open_city(browser)
    open_building(browser, 32)
    btn = browser.find("//button[contains(@class, 'sendTroops')]")
    browser.click(btn, 2)

    input = browser.find(
        "//div[@class='modalContent']")
    input = input.find_element_by_xpath(
        ".//input[contains(@class, 'targetInput')]")
    input.send_keys("({}|{})".format(x, y))
    browser.sleep(1)

    btn = browser.find(
        "//div[contains(@class, 'clickableContainer missionType4')]")
    browser.click(btn)

    units = units.split(",")

    input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
    input = input.find_elements_by_xpath(".//td")
    input = input[int(units[0])]
    input = input.find_element_by_xpath(".//input")

    input.send_keys(units[1])

    btn = browser.find("//button[contains(@class, 'next clickable')]")
    browser.click(btn, 1)
    btn = browser.find(
        "//button[contains(@class, 'sendTroops clickable')]")
    browser.click(btn, 1)

    log("Farm sent: ({}/{}).".format(x, y))

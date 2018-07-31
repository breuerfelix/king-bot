from .custom_driver import client, use_browser
from .settings import settings
import time
from .utils import log, check_for_lines
from .village import open_building, open_city, open_village
from .util_game import close_modal
import schedule
from threading import Thread
from random import randint


def start_farming_thread(browser: client, village: int, farmlists: list, interval: int) -> None:
    # todo exit when in beginners protection
    time.sleep(randint(0, 10))  # starting sleep timer

    while True:
        start_farming(browser, village, farmlists)
        time.sleep(interval + randint(0, 10))  # randomize intervals


@use_browser
def start_farming(browser: client, village: int, farmlists: list) -> None:
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


def sort_danger_farms_thread(browser: client, farmlists: list, to_list: int, red: bool, yellow: bool, interval: int) -> None:
    time.sleep(randint(0, 10))  # random sleeping at start

    while True:
        sort_danger_farms(browser, farmlists, to_list, red, yellow)
        time.sleep(interval + randint(0, 10))  # randomized intervals
# endregion


@use_browser
def sort_danger_farms(browser: client, farmlists: list, to_list: int, red: bool, yellow: bool) -> None:
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

                        print("moved one farm")
            except:
                # farm never got sent
                pass

        # press back button
        btnback = browser.find(
            "//div[@class='back clickable']")
        browser.click(btnback, 1)

    close_modal(browser)
    print("sorting farms going to sleep")


def start_custom_farmlist_thread(browser: client, reload: bool, interval: int = 60) -> None:
    # thread that executes jobs
    Thread(target=run_jobs).start()

    jobs: list = []  # current jobs

    while True:
        job_dict = check_for_lines(
            path=settings.farmlist_path, current_lines=jobs)

        # remove jobs that are not present anymore
        for rem_job in job_dict['remove']:
            schedule.clear(rem_job)
            jobs.remove(rem_job)

        # add new jobs
        for add_job in job_dict['add']:
            args = add_job.split(";")

            units = args[4]
            unit_list = units.split(",")
            unit_dict = {}

            for i in range(0, len(unit_list), 2):
                unit_dict[int(unit_list[i])] = int(unit_list[i + 1])

            # shedule task
            schedule.every(int(args[2])).seconds.do(
                send_farm, browser=browser, x=args[0], y=args[1], village=args[3], units=unit_dict).tag(add_job)

            jobs.append(add_job)
            print("job " + add_job + " started")

        browser.use()

        for add_job in job_dict['add']:
            args = add_job.split(";")

            units = args[4]
            unit_list = units.split(",")
            unit_dict = {}

            for i in range(0, len(unit_list), 2):
                unit_dict[int(unit_list[i])] = int(unit_list[i + 1])

            # send one time at start
            send_farm(browser=browser, x=args[0],
                      y=args[1], village=args[3], units=unit_dict)

        browser.done()

        if not reload:
            break

        time.sleep(interval)


@use_browser
def send_farm(browser: client, village: int, x: int, y: int, units: dict) -> None:
    log("sending units to: ({}/{}) ...".format(x, y))

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

    input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
    input = input.find_elements_by_xpath(".//td")

    units_sent = False

    if -1 in units:
        # send all units, max count
        log("send all units max count...")
        for inp in input:
            inp = inp.find_element_by_xpath(".//input")
            dis = inp.get_attribute("disabled")
            if not dis:
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

                inp.send_keys(units_to_send)
                units_sent = True

    if not units_sent:
        log("no units got sent...")
        close_modal(browser)
        return

    browser.sleep(1)
    btn = browser.find("//button[contains(@class, 'next clickable')]")
    browser.click(btn, 1)
    btn = browser.find(
        "//button[contains(@class, 'sendTroops clickable')]")
    browser.click(btn, 1)

    log("units sent to: ({}/{}).".format(x, y))


def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

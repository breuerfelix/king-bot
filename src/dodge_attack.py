from .custom_driver import client, use_browser
import time
from random import randint
from .utils import log
from .village import open_village, open_city, open_building
from .farming import send_farm
from .util_game import close_modal, shortcut, open_shortcut, check_resources, old_shortcut
from .settings import settings
import json


def check_for_attack_thread(browser: client, village: int, interval: int, units: list, target: list, save_resources: bool, units_train: list) -> None:
    time.sleep(randint(0, 10))

    if save_resources:
        with open(settings.units_path, 'r') as f:
            content = json.load(f)

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

                if save_resources:
                    save_resources_gold(browser, units_train, content)

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
def save_resources(browser: client, threshold: list) -> None:
    open_shortcut(browser, shortcut.barrack)
    el = browser.find("//div[@class='modalContent']")
    max_button = el.find_element_by_xpath(
        ".//div[@class='iconButton maxButton clickable']")
    browser.click(max_button, 1)
    browser.sleep(1)
    train_button = browser.find(
        "//button[contains(@class, 'animate footerButton')]")
    browser.click(train_button, 1)
    close_modal(browser)
    # put resource left to market based on threshold
    browser.sleep(1)
    resource = check_resources(browser)
    foo = 0
    open_shortcut(browser, shortcut.marketplace)
    browser.sleep(1)
    el = browser.find("//div[@class='modalContent']")
    sell_tab = el.find_element_by_xpath(
        ".//a[contains(@class, 'naviTabSell clickable')]")
    browser.click(sell_tab, 1)
    merchant = el.find_element_by_xpath(
        ".//div[@class='marketplaceHeaderGroup']")
    merchant = merchant.find_element_by_xpath(".//div[@class='circle']/span")
    merchant = int(merchant.get_attribute("innerHTML"))
    browser.sleep(1)
    if merchant > 0:
        for res_name in resource.keys():
            if resource[res_name] >= threshold[foo]:
                offering = browser.find("//div[@class='offerBox']")
                offering = offering.find_element_by_xpath(
                    ".//div[@class='resourceFilter filterBar']")
                offering_type = offering.find_elements_by_xpath(
                    ".//a[contains(@class, 'filter iconButton')]")
                browser.click(offering_type[foo], 1)
                input_offering = browser.find(
                    "//input[@id='marketNewOfferOfferedAmount']").send_keys("1000")
                browser.sleep(1)
                searching = browser.find("//div[@class='searchBox']")
                searching = searching.find_element_by_xpath(
                    ".//div[@class='resourceFilter filterBar']")
                searching_type = searching.find_elements_by_xpath(
                    ".//a[contains(@class, 'filter iconButton')]")
                browser.click(searching_type[(foo+1) % 2], 1)
                input_searching = browser.find(
                    "//input[@id='marketNewOfferSearchedAmount']").send_keys("2000")
                browser.sleep(1)
                while resource[res_name] >= threshold[foo] and merchant > 0:
                    sell_btn = browser.find(
                        "//button[contains(@class, 'createOfferBtn')]")
                    browser.click(sell_btn, 1)
                    resource[res_name] -= 1000
                    merchant -= 1
            browser.sleep(1)
            foo += 1
    browser.sleep(1)
    close_modal(browser)

@use_browser
def save_resources_gold(browser: client, units_train: list, content: dict) -> None:
    tribe_id = browser.find(
        '//*[@id="troopsStationed"]//li[contains(@class, "tribe")]')
    tribe_id = tribe_id.get_attribute('tooltip-translate')

    units_cost = [] #resources cost for every unit in units_train
    total_units_cost = [] #total resources cost for every unit in units_train
    training_queue: dict = {} #dict for training queue
    for tribe in content['tribe']:
        if tribe_id in tribe['tribeId']:
            for unit in tribe['units']:
                if unit['unitId'] in units_train:
                    units_cost.append(unit['trainingCost'])
                    training_cost = sum(unit['trainingCost'].values())
                    total_units_cost.append(training_cost)
                    #initializing training_queue
                    training_queue[unit['unitTrain']] = {}
                    training_queue[unit['unitTrain']][unit['unitId']] = 0

    resources = check_resources(browser)
    total_resources = sum(resources.values())

    # training amount distributed by: equal resources consumption per unit type
    training_amount = [] #amount of troop for training
    for cost in total_units_cost:
        train_amount = total_resources // (len(units_train)*cost)
        training_amount.append(train_amount)

    # fetching training_amount to training_queue
    _iter = (x for x in training_amount) #generator of training_amount
    for unit_train in training_queue:
        for unit_id in training_queue[unit_train]:
            training_queue[unit_train][unit_id] = next(_iter)

    total_training_cost = [] #amount of troop * units_cost
    _iter = (x for x in training_amount) #generator of training_amount
    for unit_cost in units_cost:
        amount = next(_iter)
        temp = {} #temporary dict
        for _keys, _values in unit_cost.items():
            temp[_keys] = _values*amount
        total_training_cost.append(temp)

    wood, clay, iron = 0, 0, 0
    for resource in total_training_cost:
        wood += resource['wood']
        clay += resource['clay']
        iron += resource['iron']

    _resource = (x for x in (wood, clay, iron)) #generator of resources
    # NPC the resources through the marketplace
    open_shortcut(browser, shortcut.marketplace)
    npc_tab = browser.find(
        '//*[@id="optimizely_maintab_NpcTrade"]')
    browser.click(npc_tab, 1)

    market_content = browser.find(
        '//div[contains(@class, "marketContent npcTrader")]')
    trs = market_content.find_elements_by_xpath(
        './/tbody[@class="sliderTable"]/tr')
    browser.sleep(1)

    for tr in trs[:-2]:
        input = tr.find_element_by_xpath(
            './/input')
        browser.sleep(0.5)
        input.clear()
        browser.sleep(1.5)
        input.send_keys(next(_resource))
        browser.sleep(1.5)
        lock = tr.find_element_by_xpath(
            './/div[@class="lockButtonBackground"]')
        browser.sleep(1.5)
        browser.click(lock, 1)
        browser.sleep(1.5)
    convert_button = market_content.find_element_by_xpath(
        './/div[@class="merchantBtn"]/button')
    browser.click(convert_button, 1)

    # close marketplace
    close_modal(browser)

    # Start training troops
    for unit_train in training_queue:
        old_shortcut(browser, unit_train)
        for unit_id in training_queue[unit_train]:
            #click picture based unit_id
            unit_type = 'unitType{}'.format(unit_id)
            image_troop = browser.find(
                "//div[@class='modalContent']//img[contains(@class, '{}')]".format(unit_type))
            browser.click(image_troop, 1)
            #input amount based training_queue[unit_train][unit_id]
            input_troop = browser.find(
                '//div[@class="inputContainer"]')
            input_troop = input_troop.find_element_by_xpath(
                './input').send_keys(training_queue[unit_train][unit_id])
            browser.sleep(1.5)
            #click train button
            train_button = browser.find(
                "//button[contains(@class, 'animate footerButton')]")
            browser.click(train_button, 1)
            browser.sleep(1.5)
        browser.sleep(1)
        close_modal(browser)

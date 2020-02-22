from .custom_driver import client, use_browser
import time
import json
from .utils import log
from .util_game import close_modal, check_resources, old_shortcut
from .village import open_village, open_city
from .settings import settings
from .worker import worker

def train_troops_thread(thread: worker, browser: client, village: int, units: list, interval: int) -> None:
    # init delay
    time.sleep(2)

    with open(settings.units_path, 'r') as f:
        content = json.load(f)

    while True:
        thread.wait()
        thread.pause()
        log("start training troops.")
        open_village(browser, village)
        open_city(browser)
        if not start_training(browser, units, content):
            log("not enough resources to train all types.")
            log("will try to use the remaining resources to train only with the first type.")
            units = [units[0]]
            if not start_training(browser, units, content):
                log("village is too low of resources.")
        
        log("finished training troops.")
        thread.resume()
        time.sleep(interval)


@use_browser
def start_training(browser: client, units_train: list, content: dict) -> bool:
    tribe_id = browser.find(
        '//*[@id="troopsStationed"]//li[contains(@class, "tribe")]')
    tribe_id = tribe_id.get_attribute('tooltip-translate')

    total_units_cost_wood = [] #total wood cost for every unit in units_train
    total_units_cost_clay = [] #total clay cost for every unit in units_train
    total_units_cost_iron = [] #total iron cost for every unit in units_train
    training_queue: dict = {} #dict for training queue
    for tribe in content['tribe']:
        if tribe_id in tribe['tribeId']:
            for unit in tribe['units']:
                if unit['unitId'] in units_train:
                    training_cost_wood = unit['trainingCost']['wood']
                    training_cost_clay = unit['trainingCost']['clay']
                    training_cost_iron = unit['trainingCost']['iron']                    
                    total_units_cost_wood.append(training_cost_wood)
                    total_units_cost_clay.append(training_cost_clay)
                    total_units_cost_iron.append(training_cost_iron)
                    #initializing training_queue
                    training_queue[unit['unitTrain']] = {}
                    training_queue[unit['unitTrain']][unit['unitId']] = {}
                    training_queue[unit['unitTrain']][unit['unitId']]['amount'] = 0
                    training_queue[unit['unitTrain']][unit['unitId']]['name'] = unit['unitName']

    resources = check_resources(browser)

    # training amount distributed by: less resources consumption per unit type
    training_amount = [] #less posible amount of troop for training
    training_amount_wood = []
    training_amount_clay = []
    training_amount_iron = []
    for cost in total_units_cost_wood:
        train_amount = resources['wood'] // (len(units_train)*cost)
        training_amount_wood.append(train_amount)

    for cost in total_units_cost_clay:
        train_amount = resources['clay'] // (len(units_train)*cost)
        training_amount_clay.append(train_amount)

    for cost in total_units_cost_iron:
        train_amount = resources['iron'] // (len(units_train)*cost)
        training_amount_iron.append(train_amount)

    # get the minimum possible troops to train
    training_amount = list(map(min, training_amount_wood, training_amount_clay, training_amount_iron))

    if sum(training_amount) == 0:
        return False

    # fetching training_amount to training_queue
    _iter = (x for x in training_amount) #generator of training_amount
    for unit_train in training_queue:
        for unit_id in training_queue[unit_train]:
            training_queue[unit_train][unit_id]['amount'] = next(_iter)

    # Start training troops
    for unit_train in training_queue:
        old_shortcut(browser, unit_train)
        for unit_id in training_queue[unit_train]:
            #input amount based training_queue[unit_train][unit_id]
            input_amount = training_queue[unit_train][unit_id]['amount']
            input_name = training_queue[unit_train][unit_id]['name']
            if input_amount == 0:
                continue # Skip empty amount
            log("training {} units of type {}".format(input_amount, input_name) + ".")
            #click picture based unit_id
            unit_type = 'unitType{}'.format(unit_id)
            image_troop = browser.find(
                "//div[@class='modalContent']//img[contains(@class, '{}')]".format(unit_type))
            browser.click(image_troop, 1)
            input_troop = browser.find(
                '//div[@class="inputContainer"]')
            input_troop = input_troop.find_element_by_xpath(
                './input')
            input_troop.click()
            input_troop.send_keys(input_amount)
            browser.sleep(1.5)
            #click train button
            train_button = browser.find(
                "//button[contains(@class, 'animate footerButton')]")
            browser.click(train_button, 1)
            browser.sleep(1.5)
        browser.sleep(1)
        close_modal(browser)
    return True

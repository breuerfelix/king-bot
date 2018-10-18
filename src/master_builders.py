from .custom_driver import client, use_browser
from .village import open_village, open_city, open_resources
from .utils import log, parse_time_to_seconds
from .settings import *
import time
import json
import os

def master_builder_thread(browser: client, village: int, file_name: str, interval:int) -> None:
    default_interval = interval
    with open(settings.buildings_path, 'r') as f:
        content = json.load(f)
    buildings = [x for x in content['buildings']]
    file_path = os.path.join(BASE_DIR, 'assets', file_name)
    # BASE_DIR come from settings.py
    while True:
        with open(file_path, 'r') as f:
            content = json.load(f)
        queues = [x for x in content['queues']]
        construct_slot, queue_slot = check_building_queue(browser, village)
        if queues and (construct_slot or queue_slot):
            while construct_slot or queue_slot:
                queues = master_builder(browser, village, queues, buildings)
                construct_slot, queue_slot = check_building_queue(browser, village)
                if not queue_slot:
                    break
                if not queues:
                    break
            with open(file_path, 'w') as f:
                f.write('{"queues":')
                f.write(json.dumps(queues, indent=4))
                f.write('}')
            interval = check_queue_times(browser, village, default_interval)
            time.sleep(interval)
        else:
            if not queues:
                log('Queues is empty, please add queue to {}'.format(file_name))
                log(time.strftime('%H:%M'))
                time.sleep(default_interval)
            else:
                time.sleep(default_interval)

@use_browser
def master_builder(browser: client, village: int, queues: list, buildings: list) -> list:
    open_village(browser, village)
    if 'Village' in queues[0]['queueLocation'] and 'Upgrade' in queues[0]['queueType']:
        open_city(browser)
        time.sleep(1)
        for building in buildings:
            if queues[0]['queueBuilding'] in building['buildingName']:
                building_id = building['buildingId']
                break
        building_img = browser.find(
            '//img[contains(@class, "{}")]/following::span'.format(building_id))
        building_status = building_img.find_element_by_xpath(
            './div')
        color = building_status.find_element_by_xpath(
            './div/div').get_attribute('class')
    if 'Resources' in queues[0]['queueLocation']:
        open_resources(browser)
        time.sleep(1)
        location_id = queues[0]['queueBuilding']
        building_location = browser.find(
            '//building-location[@class="buildingLocation {}"]'.format(location_id))
        building_status = building_location.find_element_by_xpath(
            './/div[contains(@class, "buildingStatus")]')
        color = building_status.find_element_by_xpath(
            './/div[contains(@class, "colorLayer")]').get_attribute('class')
    if 'possible' in color: #green
        browser.click_v2(building_status, 1) #use browser.click didn't click
        queues = queues[1:]
        return queues
    if 'notNow' in color: #green / yellow
        construct_slot, queue_slot = check_building_queue(browser, village)
        if queue_slot:
            browser.click_v2(building_status, 1) #use browser.click didn't click
            queues = queues[1:]
            return queues
        else:
            return queues
    if 'notAtAll' in color: #grey
        queues = queues[1:]
        return queues
    if 'maxLevel' in color: #blue
        queues = queues[1:]
        return queues

@use_browser
def check_queue_times(browser: client, village: int, default_interval: int) -> int:
    open_village(browser, village)
    construct_slot, queue_slot = check_building_queue(browser, village)
    if construct_slot:
        return default_interval
    # writedown the time
    building_queue_container = browser.find(
        '//div[contains(@class, "buildingQueueContainer queueContainer")]')
    divs = building_queue_container.find_elements_by_xpath(
        './div')
    for div in divs:
        the_class = div.get_attribute('drop-class')
        if not the_class:
            continue
        else:
            if 'noDrop' in the_class:
                browser.click(div, 1)
                inner_box = browser.find(
                    '//div[@class="detailsInnerBox"]')
                details_contents = inner_box.find_elements_by_xpath(
                    './div[contains(@class, "detailsContent")]')
                times = []
                for details_content in details_contents:
                    details_info = details_content.find_element_by_xpath(
                        './div[contains(@class, "detailsInfo")]')
                    details_time = details_info.find_element_by_xpath(
                        './div[@class="detailsTime"]')
                    span = details_time.find_element_by_xpath('./span')
                    the_time = span.get_attribute('innerHTML')
                    times.append(the_time)
                break
            else:
                continue
    # parse time to seconds
    times_in_seconds = []
    for time in times:
        time_in_seconds = parse_time_to_seconds(time)
        times_in_seconds.append(time_in_seconds)
    # return lowest time
    return min(times_in_seconds) + 3

@use_browser
def check_building_queue(browser: client, village: int) -> tuple:
    open_village(browser, village)
    # check how much construction slot that empty
    empty_construct_slot = 0
    construction_container = browser.find(
        '//div[@class="constructionContainer"]')
    building_queue_slots = construction_container.find_elements_by_xpath(
        './div')
    for building_queue_slot in building_queue_slots:
        the_class = building_queue_slot.get_attribute('class')
        if 'paid' in the_class:
            continue
        empty_construct_slot += 1
    # check how much queue slot that empty
    empty_queue = 0
    builder_container = browser.find(
        '//div[@class="masterBuilderContainer"]')
    queue_slots = builder_container.find_elements_by_xpath(
        './div')
    for queue_slot in queue_slots:
        the_class = queue_slot.get_attribute('class')
        if 'empty' not in the_class or 'locked' in the_class:
            continue
        empty_queue += 1
    return empty_construct_slot, empty_queue

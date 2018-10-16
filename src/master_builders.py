from .custom_driver import client, use_browser
from .village import open_village, open_city, open_resources
from .utils import log
from .settings import *
import time
import json
import os

def master_builder_thread(browser: client, village: int, file_name: str, interval:int) -> None:
    default_interval = interval

    with open(settings.buildings_path, 'r') as f:
        content = json.load(f)
    buildings = []
    for building in content['buildings']:
        buildings.append(building)

    while True:
        queue_path = os.path.join(BASE_DIR, "assets", file_name)
        #BASE_DIR come from settings.py
        with open(queue_path, 'r') as f:
            queue_file = json.load(f)
        queues = []
        for queue in queue_file['queues']:
            queues.append(queue)

        if queues:
            master_builder(browser, village, buildings, queues)
            interval = check_queue_times(browser)
            time.sleep(interval)
        else:
            log('Queues is empty, please add queue to {}'.format(file_name))
            log(time.strftime('%H:%M'))
            time.sleep(default_interval)

@use_browser
def master_builder(browser: client, village: int, buildings: list, queues: list) -> None:
    open_village(browser, village)
    for queue in queues:
        # check queue location
        if 'Village' in queue['queueLocation']:
            open_city(browser) #open village view
        elif 'Resources' in queue['queueLocation']:
            open_resources(browser) #open resources view
        # check queue type
        if 'Upgrade' in queue['queueType']:
            #TODO create upgrade function
            pass
        elif 'Construct' in queue['queueType']:
            #TODO create construct function
            pass
    return
    
@use_browser
def check_queue_times(browser: client) -> int:
    pass

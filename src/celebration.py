import time
from .utils import log, parse_time_to_seconds
from .custom_driver import client, use_browser
from .util_game import close_modal, open_village_overview, overview


def celebration_thread(browser: client, villages: list, celebration_type: int, interval: int) -> None:
    # init delay
    time.sleep(2)

    while True:
        sleep_time = interval
        remaining_time = manage_celebration(browser, villages, celebration_type)

        if remaining_time < interval:
            sleep_time = remaining_time + 5

        time.sleep(sleep_time)


@use_browser
def manage_celebration(browser: client, villages: list, celebration_type: int) -> int:
    available_villages = get_available_villages(browser, villages)
    log(available_villages)
    
    for village in available_villages:
        start_celebration(browser, village, celebration_type)

    lowest_time = -1
    remaining_time_list = get_celebration_times(browser, villages)

    for time in remaining_time_list:
        seconds = parse_time_to_seconds(time)

        if lowest_time == -1:
            lowest_time = seconds
            continue

        if seconds < lowest_time:
            lowest_time = seconds

    return lowest_time

def get_available_villages(browser: client, villages: list) -> list:
    open_village_overview(browser, overview.culture_points)

    tab_content = browser.find("//div[contains(@class, 'tabCulturePoints')]")
    table = tab_content.find_element_by_xpath(".//table[contains(@class, 'villagesTable')]/tbody")

    trs = table.find_elements_by_xpath(".//tr")
    
    available_villages = []
    for village in villages:
        if len(trs) <= village:
            log(f"couldn't access village: {village}")
            continue

        # village is available
        span = trs[village].find_elements_by_xpath('.//td')[2]
        span = span.find_element_by_xpath('.//span')

        ngif = span.get_attribute('ng-if')

        if "== 0" in ngif:
            available_villages.append(village)

    return available_villages

def start_celebration(browser: client, village: int, celebration_type: int) -> None:
    open_village_overview(browser, overview.culture_points)

    tab_content = browser.find("//div[contains(@class, 'tabCulturePoints')]")
    table = tab_content.find_element_by_xpath(".//table[contains(@class, 'villagesTable')]/tbody")

    trs = table.find_elements_by_xpath(".//tr")
    
    if len(trs) <= village:
        log(f"couldn't access village: {village}")
        return

    # village is available
    span = trs[village].find_elements_by_xpath('.//td')[2]
    span = span.find_element_by_xpath('.//span')

    ngif = span.get_attribute('ng-if')

    if "== 0" not in ngif:
        log(f"can't start celebration in village: {village}")
        return

    # start celebrating
    atag = span.find_element_by_xpath('.//a')
    browser.click(atag, 1)
    
    if celebration_type == 1:
        # TODO select big celebration here
        pass
        
    button = browser.find("//button[contains(@clickable, 'startCelebration')]")
    btnClasses = button.get_attribute('class')

    if 'disabled' in btnClasses:
        log(f"not enough resources to start celebration in village: {village}")
        close_modal(browser)
        return

    browser.click(button, 1)
    close_modal(browser)

def get_celebration_times(browser: client, villages: list) -> list:
    open_village_overview(browser, overview.culture_points)

    tab_content = browser.find("//div[contains(@class, 'tabCulturePoints')]")
    table = tab_content.find_element_by_xpath(".//table[contains(@class, 'villagesTable')]/tbody")

    trs = table.find_elements_by_xpath(".//tr")

    sleep_time_list = []    
    for village in villages:
        if len(trs) <= village:
            log(f"couldn't access village: {village}")
            continue

        # village is available
        span = trs[village].find_elements_by_xpath('.//td')[2]
        span = span.find_element_by_xpath('.//span')

        ngif = span.get_attribute('ng-if')

        if '> 0' in ngif:
            span = span.find_element_by_xpath('.//span')
            time = span.get_attribute('innerHTML')
            sleep_time_list.append(time)

    return sleep_time_list

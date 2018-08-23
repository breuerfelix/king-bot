from .custom_driver import client, use_browser
from threading import Thread
import time
from .utils import log
from .util_game import close_modal


def adventures_thread(browser: client, interval: int, health: int) -> None:
    # init delay
    time.sleep(2)

    while True:
        if check_health(browser, health):
            start_adventure(browser)
        else:
            log("hero is too low for adventures")

        time.sleep(interval)


@use_browser
def start_adventure(browser: client) -> None:
    #log("adventure thread waking up")

    heroLinks = browser.find("//div[@class='heroLinks']")
    a = heroLinks.find_element_by_xpath(
        ".//a[contains(@class, 'adventureLink')]")
    browser.click(a, 2)
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(
        ".//button")

    classes = el.get_attribute("class").split(" ")
    available = True

    for c in classes:
        if c == "disabled":
            available = False
            break

    if available:
        browser.click(el, 2)
        log("adventure started")

    close_modal(browser)
    #log("adventure thread sleeping")


@use_browser
def check_health(browser: client, health: int) -> bool:

    hero_stats = browser.find("//div[@class='heroStats']")
    hero_stats = hero_stats.find_element_by_xpath(
        ".//div[contains(@class, 'health')]")
    hero_health = int(hero_stats.get_attribute("perc"))

    return hero_health > health

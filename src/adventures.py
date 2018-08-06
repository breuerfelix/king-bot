from .custom_driver import client, use_browser
from threading import Thread
import time
from .utils import log
from .util_game import close_modal


def adventures_thread(browser: client, interval: int, repetition: int, health: int) -> None:
    # init delay
    time.sleep(2)

    HeroAvailable = True
    while HeroAvailable:

        if repetition > 0:
            while repetition > 0:
                HeroAvailable = CheckHero(browser, health)
                if not HeroAvailable:
                    log("Hero not well")
                    break
                repetition = start_adventure(browser, repetition)
                time.sleep(interval)
        else :
            while True:
                HeroAvailable = CheckHero(browser, health)
                if not HeroAvailable:
                    log("Hero not well")
                    break
                start_adventure(browser, repetition)
                time.sleep(interval)

        HeroAvailable = True
        time.sleep(interval)

@use_browser
def start_adventure(browser: client, repetition) -> None:
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
        repetition -= 1
    close_modal(browser)
    return repetition
    #log("adventure thread sleeping")

@use_browser
def CheckHero(browser: client, health) -> None:

    heroStats = browser.find("//div[@class='heroStats']")
    heroStats = heroStats.find_element_by_xpath(".//div[contains(@class, 'health')]")
    heroHealth = int(heroStats.get_attribute("perc"))

    if heroHealth > health:
        return True

    else:
        return False

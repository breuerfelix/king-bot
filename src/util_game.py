from .custom_driver import client
from .utils import log
from enum import Enum


def close_modal(browser: client) -> None:
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(".//a[@class='closeWindow clickable']")
    browser.click(el)


def close_welcome_screen(browser: client) -> None:
    wc = browser.find("//div[contains(@class, 'welcomeScreen')]")
    log("closing welcome-screen")
    el = wc.find_element_by_xpath(
        ".//a[@class='closeWindow clickable']")
    browser.click(el)


def check_resources(browser: client) -> dict:
    resources_list = ["wood", "clay", "iron", "crop"]
    resources = {}
    for res in resources_list:
        find_resources = browser.find(
            "//div[@class='stockContainer {0}']".format(res))
        find_resources = find_resources.find_element_by_xpath(
            ".//div[contains(@class, 'progressbar')]")
        value = int(find_resources.get_attribute("value"))
        resources[res] = value
    return resources


class shortcut(Enum):
    marketplace = 0
    barrack = 1
    stable = 2
    workshop = 3


def open_shortcut(browser: client, sc: shortcut) -> None:
    shortcut_link = browser.find("//div[@id='quickLinks']")
    shortcut_link = shortcut_link.find_element_by_xpath(
        ".//div[contains(@class, 'slotWrapper')]")
    link = shortcut_link.find_elements_by_xpath(
        ".//div[contains(@class, 'slotContainer')]")
    browser.click(link[sc.value], 1)

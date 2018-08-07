from .custom_driver import client
from .utils import log


def close_modal(browser: client):
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(".//a[@class='closeWindow clickable']")
    browser.click(el)


def close_welcome_screen(browser: client):
    wc = browser.find("//div[contains(@class, 'welcomeScreen')]")
    log("closing welcome-screen")
    el = wc.find_element_by_xpath(
        ".//a[@class='closeWindow clickable']")
    browser.click(el)


def check_resources(browser: client):
    resources_list = ["wood", "clay", "iron", "crop"]
    resources = {}
    for res in resources_list:
        find_resources = browser.find("//div[@class='stockContainer {0}']".format(res))
        find_resources = find_resources.find_element_by_xpath(".//div[contains(@class, 'progressbar')]")
        value = int(find_resources.get_attribute("value"))
        resources[res] = value
    return resources

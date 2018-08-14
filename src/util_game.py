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


def check_resources(browser: client) -> {}:
    resources_list = ["wood", "clay", "iron", "crop"]
    resources = {}
    for res in resources_list:
        find_resources = browser.find("//div[@class='stockContainer {0}']".format(res))
        find_resources = find_resources.find_element_by_xpath(".//div[contains(@class, 'progressbar')]")
        value = int(find_resources.get_attribute("value"))
        resources[res] = value
    return resources

def shortcut(browser: client, shortcut: str):
    shortcut_list = {"marketplace":0, "barrack":1, "stable":2, "workshop":3}
    shortcut_list = shortcut_list[shortcut]

    shortcut_link = browser.find("//div[@id='quickLinks']")
    shortcut_link = shortcut_link.find_element_by_xpath(".//div[contains(@class, 'slotWrapper')]")
    link = shortcut_link.find_elements_by_xpath(".//div[contains(@class, 'slotContainer')]")

    browser.click(link[shortcut_list], 1)

def village_list(browser: client) -> []:
    villages_list = []
    ul = browser.find("//div[contains(@class, 'villageListDropDown')]")
    ul = ul.find_element_by_xpath(".//ul")
    lis = ul.find_elements_by_xpath(".//li")
    for village in lis:
        village_name = village.find_element_by_xpath(".//div[contains(@class, 'villageEntry')]")
        village_name = village_name.get_attribute("innerHTML")
        villages_list.append(village_name)
    return villages_list

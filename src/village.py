from .utils import log
from .util_game import close_modal
from .custom_driver import client

# todo check if already in village/city or ress


def open_village(browser: client, id: int):
    index = id

    btn = browser.find("//a[@id='villageOverview']")
    browser.click(btn, 1)
    table = browser.find(
        "//table[contains(@class, 'villagesTable')]/tbody")
    villages = table.find_elements_by_xpath(".//tr")

    tds = villages[index].find_elements_by_xpath(".//td")
    link = tds[0].find_element_by_xpath(".//a")
    browser.click(link, 1)

    log("opened village {}".format(index))
    close_modal(browser)


def open_city(browser: client):
    btn = browser.find("//a[@id='optimizly_mainnav_village']")
    browser.click(btn, 1)


def open_resources(browser: client):
    btn = browser.find("//a[@id='optimizly_mainnav_resources']")
    browser.click(btn, 1)


def open_building(browser: client, building: int):
    # todo open by slot id
    img = browser.find(
        "//img[@id='buildingImage{}']".format(building))
    browser.click(img, 1)

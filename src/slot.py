from .utils import log
from .custom_driver import client
from selenium.webdriver.remote import webelement


def find_slot(browser: client, id: int) -> webelement:
    el_list = browser.driver.find_elements_by_xpath(
        "//div[contains(@class, 'buildingStatus location{}')]".format(id))

    for element in el_list:
        c = element.get_attribute("class")
        classes = c.split(" ")
        for cla in classes:
            if cla == "location{}".format(id):
                return element

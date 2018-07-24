from .customDriver import client


def closeModal(browser: client):
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(".//a[@class='closeWindow clickable']")
    browser.click(el)


def log(message: str):
    print(message)

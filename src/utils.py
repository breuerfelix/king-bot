def closeModal(browser):
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(".//a[@class='closeWindow clickable']")
    browser.click(el)


def log(string):
    print(string)


def openResources(browser):
    btn = browser.find("//a[@id='optimizly_mainnav_resources']")
    browser.click(btn)


def openVillage(browser):
    btn = browser.find("//a[@id='optimizly_mainnav_village']")
    browser.click(btn)

def closeModal(browser):
    el = browser.find("//div[@class='modalContent']")
    el = el.find_element_by_xpath(".//a[@class='closeWindow clickable']")
    browser.click(el)


def log(string):
    print(string)

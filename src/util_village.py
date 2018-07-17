from .utils import closeModal, log


def openVillage(browser, id):
    index = int(id)

    btn = browser.find("//a[@id='villageOverview']")
    browser.click(btn)
    browser.sleep(0.5)
    table = browser.find(
        "//table[contains(@class, 'villagesTable')]/tbody")
    villages = table.find_elements_by_xpath(".//tr")

    tds = villages[index].find_elements_by_xpath(".//td")
    link = tds[0].find_element_by_xpath(".//a")
    browser.click(link)
    browser.sleep(1)

    log("opened village {}".format(index))
    closeModal(browser)


def openCity(browser):
    btn = browser.find("//a[@id='optimizly_mainnav_village']")
    browser.click(btn)
    browser.sleep(1)


def openBuilding(browser, building):
    # todo open by slot id
    img = browser.find(
        "//img[@id='buildingImage{}']".format(building))
    browser.click(img)
    browser.sleep(1)

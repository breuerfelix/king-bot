from .utils import closeModal, log


class slot:
    def __init__(self, browser, id):
        self.browser = browser
        self.id = id
        self.upgradable = False
        self.field = id < 19
        self.lvl = -1

        # building slot
        self.free = False
        pass

    def update(self):
        el = self.findSlot()
        templvl = el.find_element_by_class_name("buildingLevel")
        self.lvl = templvl.get_attribute("innerHTML")
        temp_upgrade = el.find_element_by_xpath(
            ".//div[contains(@class, 'colorLayer')]").get_attribute("class")

        if "possible" in temp_upgrade:
            self.upgradable = True

    def upgrade(self):
        el = self.findSlot()
        el = el.find_element_by_xpath(".//div[contains(@class, 'clickable')]")
        self.browser.click(el)
        self.browser.sleep(0.5)
        self.browser.click(el)
        self.browser.sleep(0.5)

        log("added slot: {} to queue".format(self.id))

    def findSlot(self):
        el_list = self.browser.driver.find_elements_by_xpath(
            "//div[contains(@class, 'buildingStatus location{}')]".format(self.id))

        for element in el_list:
            c = element.get_attribute("class")
            classes = c.split(" ")
            for cla in classes:
                if cla == "location{}".format(self.id):
                    return element

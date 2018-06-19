from threading import Thread
import time


class gameworld:
    def __init__(self, browser, world):
        self.world = world.lower()
        self.browser = browser

        # init
        self.villages = []
        self.delayCheckAdventures = 60

        self.browser.use()
        try:
            # opens game world start
            # self.browser.get('https://{}.kingdoms.com'.format(self.world))
            # self.browser.sleep(5)
            self.closeWelcomeScreen()
        except:
            print("no welcome screen found")
        finally:
            self.browser.done()

    def closeWelcomeScreen(self):
        wc = self.browser.find("//div[contains(@class, 'welcomeScreen')]")
        print("closing welcome-screen")
        el = wc.find_element_by_xpath(
            ".//a[@class='closeWindow clickable']")
        self.browser.click(el)

    def enableAdventures(self, delay=100):
        # todo if hero is above x% health
        self.delayCheckAdventures = delay

        t = Thread(target=self.enableAdventures_thread)
        t.start()

    def enableAdventures_thread(self):
        def closeWindow():
            el = self.browser.find("//div[@class='modalContent']")
            el = el.find_element_by_xpath(
                ".//a[@class='closeWindow clickable']")
            self.browser.click(el)

        # init delay
        time.sleep(2)

        while True:
            print("adventure thread waking up")

            self.browser.use()

            try:
                heroLinks = self.browser.find("//div[@class='heroLinks']")
                a = heroLinks.find_element_by_xpath(
                    ".//a[contains(@class, 'adventureLink')]")
                self.browser.click(a)
                self.browser.sleep(2)
                el = self.browser.find("//div[@class='modalContent']")
                el = el.find_element_by_xpath(
                    ".//button")

                classes = el.get_attribute("class").split(" ")
                available = True

                for c in classes:
                    if c == "disabled":
                        available = False
                        break

                if available:
                    self.browser.click(el)
                    print("adventure started")
                    self.browser.sleep(2)

                closeWindow()
            except:
                print("error starting adventure - closing window")
                try:
                    closeWindow()
                except:
                    print("error closing window - refreshing page")
                    self.browser.get(
                        'https://{}.kingdoms.com'.format(self.world))

            self.browser.done()

            print("adventure thread sleeping")
            time.sleep(self.delayCheckAdventures)


class village:
    def __init__(self, browser):
        self.slots = []
        self.browser = browser

        self.browser.use()

        try:
            self.initResourceFields()
        except:
            print("error init village")
        finally:
            self.browser.done()

    def initResourceFields(self):
        self.openResources()
        self.browser.sleep(1)
        for i in range(1, 19):
            f = slot(self.browser, i)
            f.update()
            self.slots.append(f)

    def openResources(self):
        btn = self.browser.find("//a[@id='optimizly_mainnav_resources']")
        self.browser.click(btn)

    def openVillage(self):
        btn = self.browser.find("//a[@id='optimizly_mainnav_village']")
        self.browser.click(btn)

    def upgrade(self, slotnumber):
        slot = None
        for s in self.slots:
            if s.id == slotnumber:
                slot = s
                break

        self.browser.use()
        try:
            self.openResources()
            slot.upgrade()
            self.openResources()
        except:
            print("error upgrading village slot " + str(slotnumber))
        finally:
            self.browser.done()


class slot:
    def __init__(self, browser, id):
        self.browser = browser
        self.id = id
        self.upgradable = False
        pass

    def update(self):
        el = self.findSlot()
        templvl = el.find_element_by_class_name("buildingLevel")
        lvl = templvl.get_attribute("innerHTML")
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

    def findSlot(self):
        el_list = self.browser.driver.find_elements_by_xpath(
            "//div[contains(@class, 'buildingStatus location{}')]".format(self.id))

        for element in el_list:
            c = element.get_attribute("class")
            classes = c.split(" ")
            for cla in classes:
                if cla == "location{}".format(self.id):
                    return element

from threading import Thread
import time
from utils import closeModal, log
from threading import Lock
from selenium.webdriver.common.keys import Keys


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

            try:
                self.closeWelcomeScreen()
            except:
                # no welcome screen found
                pass

            self.initVillages()
        except:
            log("no welcome screen found")
        finally:
            self.browser.done()

    def initVillages(self):
        btn = self.browser.find("//a[@id='villageOverview']")
        self.browser.click(btn)
        self.browser.sleep(0.5)
        table = self.browser.find(
            "//table[contains(@class, 'villagesTable')]/tbody")
        villages = table.find_elements_by_xpath(".//tr")
        for vil in villages:
            tds = vil.find_elements_by_xpath(".//td")

            name = tds[0].find_element_by_xpath(
                ".//a").get_attribute("innerHTML")

            self.villages.append(village(self.browser, name))
            log("village {} added".format(name))

        closeModal(self.browser)

    def closeWelcomeScreen(self):
        wc = self.browser.find("//div[contains(@class, 'welcomeScreen')]")
        log("closing welcome-screen")
        el = wc.find_element_by_xpath(
            ".//a[@class='closeWindow clickable']")
        self.browser.click(el)

    # todo upgrade modes
    def upgradeSlot(self, village, slot, amount=1):
        for _ in range(amount):
            self.villages[village].upgrade(slot)

    def enableAdventures(self, delay=100):
        # todo if hero is above x% health
        # todo delay = hero back time
        self.delayCheckAdventures = delay

        t = Thread(target=self.enableAdventures_thread)
        t.start()

    def enableAdventures_thread(self):
        # init delay
        time.sleep(2)

        while True:
            log("adventure thread waking up")

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
                    log("adventure started")
                    self.browser.sleep(2)

                closeModal(self.browser)
            except:
                log("error starting adventure - closing window")
                try:
                    closeModal(self.browser)
                except:
                    log("error closing window - refreshing page")
                    self.browser.get(
                        'https://{}.kingdoms.com'.format(self.world))

            self.browser.done()

            log("adventure thread sleeping")
            time.sleep(self.delayCheckAdventures)

    def startFarming(self, village, farmlists, interval):
        self.villages[village].startFarming(farmlists, interval)


class village:
    def __init__(self, browser, name):
        self.slots = []
        self.browser = browser

        self.lock = Lock()
        self.upgradeList = []

        self.name = name

        # init resource slots
        for i in range(1, 19):
            f = slot(self.browser, i)
            self.slots.append(f)

    # todo implement if you need access to lvl of fields
    def load(self):
        self.browser.use()

        try:
            self.initResourceFields()
        except:
            log("error init village")
        finally:
            self.browser.done()

    def initResourceFields(self):
        self.openResources()
        self.browser.sleep(1)
        for slot in self.slots:
            slot.update()

    def openResources(self):
        btn = self.browser.find("//a[@id='optimizly_mainnav_resources']")
        self.browser.click(btn)

    def openVillage(self):
        btn = self.browser.find("//a[@id='optimizly_mainnav_village']")
        self.browser.click(btn)

    def openBuilding(self, building):
        img = self.browser.find(
            "//img[@id='buildingImage{}']".format(building))
        self.browser.click(img)
        self.browser.sleep(0.5)

    def upgrade(self, slotnumber):
        slot = None
        for s in self.slots:
            if s.id == slotnumber:
                slot = s
                break

        self.lock.acquire()

        if len(self.upgradeList) < 1:
            t = Thread(target=self.upgrade_thread)
            t.start()

        self.upgradeList.append(slot)
        self.lock.release()

    def checkBuildingSlot(self):
        slots = self.browser.driver.find_elements_by_xpath(
            "//div[@class='masterBuilderContainer']/div[contains(@class, 'buildingQueueSlot')]")

        freeSlots = 0
        locked = False

        for slot in slots:
            if locked:
                break

            classes = slot.get_attribute("class").split(" ")
            for c in classes:
                if "empty" == c:
                    freeSlots += 1

                if "locked" == c:
                    locked = True
                    break

        return freeSlots

    def getRemainingBuildingTime(self):
        # todo implement
        return 60

    def upgrade_thread(self):
        # init sleep time
        time.sleep(3)

        while True:
            log("building queue village {} waking up".format(self.name))
            delay = 60

            self.lock.acquire()

            self.browser.use()
            try:
                freeSlots = self.checkBuildingSlot()
                for _ in range(freeSlots):
                    self.openResources()
                    self.upgradeList[0].upgrade()
                    del self.upgradeList[0]
                    self.openResources()
            except:
                log("error upgrading village slot " +
                    str(self.upgradeList[0].id))
            finally:
                self.browser.done()

            if len(self.upgradeList) < 1:
                # shut down thread
                self.lock.release()
                break
            else:
                delay = self.getRemainingBuildingTime()

            self.lock.release()
            log("building queue village {} sleeping".format(self.name))

            # todo modify
            time.sleep(delay)

    def startFarming(self, farmlists, interval):
        t = Thread(target=self.startFarming_thread, args=[farmlists, interval])
        t.start()

    def startFarming_thread(self, farmlists, interval):
        # todo exit when in beginners protection
        time.sleep(3)

        while True:
            log("farming thread in village {} waking up".format(self.name))

            self.browser.use()

            try:
                self.openVillage()
                self.openBuilding(32)
                self.browser.sleep(1)
                tab = self.browser.find(
                    "//a[contains(@class, 'tab naviTabFarmList')]")
                self.browser.click(tab)
                self.browser.sleep(1)
                table = self.browser.find(
                    "//div[@class='farmList']")
                table = self.browser.find(
                    ".//table[contains(@class, 'farmListsOverviewTable')]")
                lists = table.find_elements_by_xpath(
                    ".//tbody")

                for i in farmlists:
                    cb = lists[i].find_element_by_xpath(
                        ".//input[@type='checkbox']")
                    # cb.send_keys(Keys.SPACE)
                    self.browser.click(cb)

                self.browser.sleep(0.5)
                btn = self.browser.find(
                    "//button[contains(@class, 'startRaid')]")
                self.browser.click(btn)
                log("farmlist sent")

                self.browser.sleep(0.5)

                closeModal(self.browser)
            except:
                log("error sending farm lists in village {}".format(self.name))
            finally:
                self.browser.done()

            log("farming thread in village {} sleeping".format(self.name))
            time.sleep(interval)


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

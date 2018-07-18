from .utils import closeModal, log, openResources, openVillage
from threading import Lock
from .slot import slot
from threading import Thread
import time
from .util_village import openVillage as openVil


class village:
    def __init__(self, browser, name, index):
        self.slots = []
        self.browser = browser

        self.lock = Lock()  # lock for accessing the upgrade list
        self.upgradeList = []

        self.name = name
        self.index = index

        # init resource slots
        for i in range(1, 19):
            f = slot(self.browser, i)
            self.slots.append(f)

        # init village slots
        for i in range(19, 41):
            s = slot(self.browser, i)
            self.slots.append(s)

    # todo implement if you need access to lvl of fields
    def load(self):
        self.browser.use()

        try:
            self.initResourceFields()
            self.initVillageSlots()
        except:
            log("error init village")
        finally:
            self.browser.done()

    def initResourceFields(self):
        openResources(self.browser)
        self.browser.sleep(1)
        for slot in self.slots:
            if slot.field:
                slot.update()

    def initVillageSlots(self):
        openVillage(self.browser)
        self.browser.sleep(1)
        for slot in self.slots:
            if slot.field == True:
                slot.update()

    def openBuilding(self, building):
        # todo open by slot id
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
                    openResources(self.browser)
                    self.upgradeList[0].upgrade()
                    del self.upgradeList[0]
                    openResources(self.browser)
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
                openVil(self.browser, self.index)
                openVillage(self.browser)
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

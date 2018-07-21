from threading import Thread
import time
import schedule
from .utils import closeModal, log
from selenium.webdriver.common.keys import Keys
from .village import village
from .util_village import openVillage, openCity, openBuilding


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

            self.villages.append(
                village(self.browser, name, villages.index(vil)))
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

    # region adventures
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
    # endregion

    # region check farms
    def sortDangerFarms(self, farmlists, toList, red=False, yellow=False, interval=240):
        t = Thread(target=self.sortDangerFarms_thread,
                   args=(farmlists, toList, red, yellow, interval))
        t.start()

    def sortDangerFarms_thread(self, farmlists, toList, red, yellow, interval):
        time.sleep(2)

        while True:
            self.browser.use()
            print("sorting farms started...")

            try:
                openCity(self.browser)
                openBuilding(self.browser, 32)

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
                    # opens farmlist
                    cb = lists[i].find_element_by_xpath(
                        ".//td[contains(@class, 'clickable')]")
                    self.browser.click(cb)

                    tbody = self.browser.find(
                        "//div[@class='listDetail']")
                    tbody = tbody.find_element_by_xpath(".//tbody")
                    trs = tbody.find_elements_by_xpath(".//tr")
                    for tr in trs:
                        tds = tr.find_elements_by_xpath(".//td")
                        try:
                            icon = tds[6].find_element_by_xpath(".//i")
                            translate = icon.get_attribute("tooltip-translate")
                            if translate != "Notification_1":
                                print("found yellow or red farm")
                                movefarm = False
                                if translate == "Notification_2":
                                    #farm is yellow
                                    if yellow == True:
                                        movefarm = True
                                elif translate == "Notification_3":
                                    #farm is red
                                    if red == True:
                                        movefarm = True

                                if movefarm == True:
                                    # move the farm
                                    self.browser.hover(tds[1])
                                    add = tds[9].find_element_by_xpath(
                                        ".//div[contains(@clickable, 'farmListAdd')]")
                                    self.browser.click(add)
                                    self.browser.sleep(1)

                                    inner = self.browser.find(
                                        "//div[@class='farmListInner']")
                                    movelists = inner.find_element_by_xpath(
                                        ".//div[contains(@class, 'list')]")

                                    # todo test this !!
                                    # move to new list
                                    self.browser.hover(movelists[toList])
                                    self.browser.click(movelists[toList])
                                    self.browser.sleep(1)

                                    # remove from current list
                                    self.browser.hover(movelists[i])
                                    self.browser.click(movelists[i])
                                    self.browser.sleep(1)

                                    modal = self.browser.find(
                                        "//div[contains(@class, 'farmListAdd')]")
                                    closemodal = modal.find_element_by_xpath(
                                        ".//a[contains(@class, 'closeWindow')]")
                                    self.browser.click(closemodal)
                                    self.browser.sleep(2)
                        except:
                            # farm never got sent
                            pass

# change notification == 1 und movefarm = true
                    # press back button
                    btnback = self.browser.find(
                        "//div[@class='back clickable']")
                    self.browser.click(btnback)
                    self.browser.sleep(1)

            except Exception as e:
                print("error in sorting farms")
                print(str(e))
                closeModal(self.browser)
                pass
            finally:
                self.browser.done()

            print("sorting farms going to sleep")
            time.sleep(interval)
        pass
    # endregion

    # region farming
    def startFarming(self, village, farmlists, interval):
        self.villages[village].startFarming(farmlists, interval)

    def startFarmlist(self, path):
        t = Thread(target=self.startFarmlist_thread,
                   args=(path,), daemon=False)
        t.start()

    def startFarmlist_thread(self, path):
        with open(path, "r") as file:
            lines = file.readlines()

        for line in lines:
            args = line.split(";")

            # shedule task
            schedule.every(int(args[2])).seconds.do(
                self.sendFarm, x=args[0], y=args[1], village=args[3], units=args[4])

        for line in lines:
            args = line.split(" ")
            # send one time at start
            self.sendFarm(x=args[0], y=args[1], village=args[3], units=args[4])

        while True:
            schedule.run_pending()
            time.sleep(1)

    def sendFarm(self, x, y, village, units):
        browser = self.browser

        browser.use()
        log("Sending farm: ({}/{}) ...".format(x, y))
        try:
            openVillage(browser, village)
            openCity(browser)
            openBuilding(browser, 32)
            btn = browser.find("//button[contains(@class, 'sendTroops')]")
            browser.click(btn)
            browser.sleep(3)

            input = browser.find(
                "//div[@class='modalContent']")
            input = input.find_element_by_xpath(
                ".//input[contains(@class, 'targetInput')]")
            input.send_keys("({}|{})".format(x, y))
            browser.sleep(1)

            btn = browser.find(
                "//div[contains(@class, 'clickableContainer missionType4')]")
            browser.click(btn)

            units = units.split(",")

            input = browser.find("//tbody[contains(@class, 'inputTroops')]/tr")
            input = input.find_elements_by_xpath(".//td")
            input = input[int(units[0])]
            input = input.find_element_by_xpath(".//input")

            input.send_keys(units[1])

            btn = browser.find("//button[contains(@class, 'next clickable')]")
            browser.click(btn)
            browser.sleep(0.5)
            btn = browser.find(
                "//button[contains(@class, 'sendTroops clickable')]")
            browser.click(btn)
            browser.sleep(0.5)

            log("Farm sent: ({}/{}).".format(x, y))
        except:
            log("Error sending farm: ({}/{}).".format(x, y))

        browser.done()
    # endregion

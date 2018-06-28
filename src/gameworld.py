from threading import Thread
import time
from .utils import closeModal, log
from selenium.webdriver.common.keys import Keys
from .village import village


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

# region farming
    def startFarming(self, village, farmlists, interval):
        self.villages[village].startFarming(farmlists, interval)
# endregion

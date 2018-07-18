from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from .utils import log
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from threading import RLock

"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""


class client:
    def __init__(self):
        self.driver = None
        self.delay = None
        self._headless = False
        self.lock = RLock()
        pass

    def chrome(self, path):
        self.driver = webdriver.Chrome(path)
        self.setConfig()
        self.saveSession()

    def remote(self, path):
        file = open(path, "r")
        content = file.read()
        lines = content.split(";")
        url = lines[0]
        session = lines[1]

        self.driver = webdriver.Remote(
            command_executor=url, desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.session_id = session

        self.setConfig()

    def headless(self, path):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('disable-gpu')

        self.driver = webdriver.Chrome(path, chrome_options=options)
        self.setConfig()
        self._headless = True

    def setConfig(self):
        # set timeout to find an element in seconds
        self.driver.implicitly_wait(5)
        # set page load timeout in seconds
        self.driver.set_page_load_timeout(10)

    # region locks
    def use(self):
        self.lock.acquire()

    def done(self):
        self.lock.release()
    # endregion

    # region browser function
    def get(self, page):
        self.driver.get(page)

    def find(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def sleep(self, seconds):
        # reduce sleep time if in headless mode
        if self._headless:
            seconds = seconds / 2

        time.sleep(seconds)

    def click(self, element):
        ActionChains(self.driver).move_to_element(element).click().perform()
        self.sleep(0.5)
    # endregion

    # region session
    def saveSession(self):
        url = self.driver.command_executor._url
        session = self.driver.session_id

        filename = './assets/currentSession.txt'
        semi = ';'

        content = url + semi + session

        try:
            file = open(filename, "w")
            file.write(content)
            file.close()
        except:
            log('Error saving Session')

    def writeSource(self):
        file = open("./source.html", "w")
        file.write(self.driver.page_source)
        file.close()
    # endregion

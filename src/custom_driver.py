from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from .utils import log
from threading import RLock
from typing import Any

"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""


def use_browser(org_func: Any):
    def wrapper(*args, **kwargs):
        browser = None
        for arg in args:
            if type(arg) is client:
                browser = arg
                break

        for _, value in kwargs.items():
            if type(value) is client:
                browser = value
                break

        if browser != None:
            rv = None
            browser.use()

            try:
                rv = org_func(*args, **kwargs)
            except Exception as e:
                rv = None
                log("exception in function: {} exception: {}".format(
                    org_func.__name__, str(e)))

                log("reloading world")
                url = browser.driver.current_url
                world = url.split('//')
                world = world[1]
                world = world.split('.')
                world = world[0]

                browser.get('https://{}.kingdoms.com'.format(world))
            finally:
                browser.done()

                return rv

        else:
            return org_func(*args, **kwargs)

    return wrapper


class client:
    def __init__(self, debug: bool = False) -> None:
        self.driver: webdriver = None
        self.delay = None
        self._headless: bool = False
        self.lock = RLock()
        self.proxy: bool = False
        self.debug: bool = debug
        self.current_session_path: str = "./assets/current_session.txt"
        pass

    def chrome(self, path: str, proxy: str = '') -> None:
        options = webdriver.ChromeOptions()
        if proxy is not "":
            self.proxy = True
            options.add_argument('proxy-server={}'.format(proxy))

        options.add_argument('window-size=1500,1200')

        self.driver = webdriver.Chrome(path, chrome_options=options)
        self.set_config()
        self.save_session()

    def remote(self) -> None:
        if not self.debug:
            log("debug mode is turned off, can't reuse old session")
            return

        file = open(self.current_session_path, "r")
        content = file.read()
        lines = content.split(";")
        url = lines[0]
        session = lines[1]

        self.driver = webdriver.Remote(
            command_executor=url, desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.session_id = session

        self.set_config()

    def headless(self, path: str, proxy: str = '') -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1500,1200')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('disable-gpu')

        if proxy is not "":
            self.proxy = True
            options.add_argument('proxy-server={}'.format(proxy))

        self.driver = webdriver.Chrome(path, chrome_options=options)
        self.set_config()
        self._headless = True

    def set_config(self) -> None:
        # set timeout to find an element in seconds
        self.driver.implicitly_wait(5)
        # set page load timeout in seconds
        self.driver.set_page_load_timeout(20)

    # region locks
    def use(self) -> None:
        self.lock.acquire()

    def done(self) -> None:
        self.lock.release()
    # endregion

    # region browser function
    def get(self, page: str) -> None:
        self.driver.get(page)

    def find(self, xpath: str, wait: float = 0) -> webelement:
        # todo wait x seconds until presencd of element
        self.sleep(wait)
        return self.driver.find_element_by_xpath(xpath)

    def sleep(self, seconds: float) -> None:
        # reduce sleep time if in headless mode
        if self._headless:
            seconds = seconds / 2

        # doubles the sleep time, proxys are normaly way slower
        if self.proxy:
            seconds = seconds * 2

        time.sleep(seconds)

    def click(self, element: webelement, wait: float = 0.5) -> None:
        ActionChains(self.driver).move_to_element(element).click().perform()
        self.sleep(wait)

    def hover(self, element: webelement, wait: float = 0.5) -> None:
        ActionChains(self.driver).move_to_element(element).perform()
        self.sleep(wait)

    def scroll_down(self, element: webelement) -> None:
        element.send_keys(Keys.PAGE_DOWN)
    # endregion

    # region session
    def save_session(self) -> None:
        if not self.debug:
            return

        url = self.driver.command_executor._url
        session = self.driver.session_id

        filename = self.current_session_path
        semi = ';'

        content = url + semi + session

        try:
            file = open(filename, "w")
            file.write(content)
            file.close()
        except:
            log('Error saving Session')

    def write_source(self) -> None:
        file = open("./source.html", "w")
        file.write(self.driver.page_source)
        file.close()
    # endregion

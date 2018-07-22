from .utils import log
from .customDriver import client


def login(browser: client, gameworld: str, email: str, password: str):
    world = gameworld

    browser.use()

    try:
        browser.get('https://kingdoms.com')

        loginButton = browser.find("//span[text()='Login']")
        browser.click(loginButton)
        browser.sleep(3)

        el = browser.find("//iframe[@class='mellon-iframe']")
        browser.driver.switch_to.frame(el)
        el = browser.find("//iframe")
        browser.driver.switch_to.frame(el)

        browser.find("//input[@name='email']").send_keys(email)
        pw = browser.find("//input[@name='password']")
        pw.send_keys(password)
        pw.submit()
        browser.sleep(3)

        checkNotification(browser)

        # login to gameworld
        browser.find(
            "//span[contains(text(), '{}')]/following::button[@type='button']".format(world)).click()
        browser.sleep(8)
    except:
        log("Failed to Login.")
        pass
    finally:
        browser.done()


def checkNotification(browser: client):
    try:
        browser.find("//body[contains(@class, 'modal-open')]")
        log('closing notification-modal')
        browser.find("//button[@class='close']").click()
        browser.sleep(1)
    except:
        pass

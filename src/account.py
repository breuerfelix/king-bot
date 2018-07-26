from .utils import log
from .custom_driver import client, use_browser


@use_browser
def login(browser: client, gameworld: str, email: str, password: str):
    world = gameworld

    browser.get('https://kingdoms.com')

    loginButton = browser.find("//span[text()='Login']")
    browser.click(loginButton)

    el = browser.find("//iframe[@class='mellon-iframe']", 3)
    browser.driver.switch_to.frame(el)
    el = browser.find("//iframe")
    browser.driver.switch_to.frame(el)

    browser.find("//input[@name='email']").send_keys(email)
    pw = browser.find("//input[@name='password']")
    pw.send_keys(password)
    pw.submit()
    browser.sleep(3)

    check_notification(browser)

    # login to gameworld
    browser.find(
        "//span[contains(text(), '{}')]/following::button[@type='button']".format(world)).click()

    log("login successful")
    browser.sleep(8)


def check_notification(browser: client):
    try:
        browser.find("//body[contains(@class, 'modal-open')]")
        log('closing notification-modal')
        btn_close = browser.find("//button[@class='close']")
        browser.click(btn_close, 1)
    except:
        pass

from utils import log


class account:
    def __init__(self, browser, email, password):
        self.email = email
        self.password = password
        self.world = ''
        self.browser = browser

    def login(self, world):
        self.world = world

        self.browser.use()

        try:
            self.browser.get('https://kingdoms.com')

            loginButton = self.browser.find("//span[text()='Login']")
            self.browser.click(loginButton)
            self.browser.sleep(3)

            el = self.browser.find("//iframe[@class='mellon-iframe']")
            self.browser.driver.switch_to.frame(el)
            el = self.browser.find("//iframe")
            self.browser.driver.switch_to.frame(el)

            self.browser.find("//input[@name='email']").send_keys(self.email)
            pw = self.browser.find("//input[@name='password']")
            pw.send_keys(self.password)
            pw.submit()
            self.browser.sleep(3)

            self.checkNotification()

            # login to gameworld
            self.browser.find(
                "//span[contains(text(), '{}')]/following::button[@type='button']".format(self.world)).click()
            self.browser.sleep(8)
        except:
            log("Failed to Login.")
            pass
        finally:
            self.browser.done()

    def checkNotification(self):
        try:
            self.browser.find("//body[contains(@class, 'modal-open')]")
            log('closing notification-modal')
            self.browser.find("//button[@class='close']").click()
            self.browser.sleep(1)
        except:
            pass

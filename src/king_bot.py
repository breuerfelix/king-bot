from .custom_driver import client
from .adventures import adventures_thread
from threading import Thread
import platform
import sys
import getopt
from .account import login
import time
from .util_game import close_welcome_screen
from .utils import log
from .farming import start_farming_thread, start_custom_farmlist_thread, sort_danger_farms_thread


class king_bot:
    def __init__(self, email: str, password: str, gameworld: str, chrome_driver_path: str, current_session_path: str, proxy: str, start_args: list):
        self.browser = None
        self.chrome_driver_path = chrome_driver_path
        self.current_session_path = current_session_path
        self.gameworld = gameworld

        # add extension if on windows
        if platform.system() == 'Windows':
            self.chrome_driver_path += '.exe'

        self.init(email=email, password=password,
                  proxy=proxy, start_args=start_args)

    def init(self, email: str, password: str, proxy: str, start_args: list):
        self.browser = client()
        login_req = True
        manual_login = False

        try:
            opts, _ = getopt.getopt(
                start_args[1:], "hmrte:p:w:", ["email=", "password=", "gameworld="])
        except:
            print("error in arguments. check github for details.")
            sys.exit()
        for opt, arg in opts:
            if opt == "-t":
                # todo run test file or type checker
                sys.exit()
            elif opt == '-h':
                self.browser.headless(self.chrome_driver_path, proxy=proxy)
            elif opt == '-r':
                self.browser.remote(self.current_session_path)
                login_req = False
            elif opt == '-m':
                login_req = False
                manual_login = True
            elif opt in ("-e", "--email"):
                email = arg
            elif opt in ("-p", "--password"):
                password = arg
            elif opt in ("-w", "--gameworld"):
                self.gameworld = arg

        if self.browser.driver == None:
            self.browser.chrome(self.chrome_driver_path, proxy=proxy)

        if login_req:
            if email == None or password == None:
                # settings path
                credentialsPath = "./assets/credentials.txt"

                # read login credentials
                file = open(credentialsPath, "r")
                text = file.read()
                file.close()

                if email == None:
                    email = text.split(";")[0]
                if password == None:
                    password = text.split(";")[1]

            close = False
            if self.gameworld == None:
                log("no gameworld provided")
                close = True

            if email == None:
                log("no email provided")
                close = True

            if password == None:
                log("no password provided")
                close = True

            if close:
                sys.exit()

            login(browser=self.browser, gameworld=self.gameworld,
                  email=email, password=password)

            # clear loging credentials
            email = None
            password = None

        if manual_login:
            self.browser.use()
            self.browser.get('https://kingdoms.com')
            time.sleep(120)
            self.browser.done()

        self.browser.use()

        try:
            close_welcome_screen(self.browser)
        except:
            pass

        self.browser.done()

    def start_adventures(self, interval: int = 100):
        Thread(target=adventures_thread, args=(self.browser, interval)).start()

    # todo implement
    def upgrade_slot(self, village: int, slot: int):
        log("upgrading slots is under construction - check for updates")

        if slot > 19:
            log("upgrading buildings is still under construction")
            return

    def start_farming(self, village: int, farmlists: list, interval: int):
        Thread(target=start_farming_thread, args=[
               self.browser, village, farmlists, interval]).start()

    def start_custom_farmlist(self, path: str):
        Thread(target=start_custom_farmlist_thread,
               args=[self.browser, path]).start()

    def sort_danger_farms(self, farmlists: list, to_list: int, red: bool, yellow: bool, interval: int):
        Thread(target=sort_danger_farms_thread, args=[
               self.browser, farmlists, to_list, red, yellow, interval]).start()

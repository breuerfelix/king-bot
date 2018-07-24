from src import client, login, gameworld
import sys
import getopt
import platform
import time


def main():
    # settings
    chromedriverPath = './assets/chromedriver'  # without extension
    currentSessionPath = './assets/currentSession.txt'

    if platform.system() == 'Windows':
        chromedriverPath += '.exe'

    world = 'COM5'  # choose uppercase (exact world name)
    email = None
    password = None
    browser = client()
    login_req = True
    manual_login = False

    try:
        opts, _ = getopt.getopt(
            sys.argv[1:], "hmrte:p:w:", ["email=", "password=", "gameworld="])
    except:
        print("error in arguments. check github for details.")
        sys.exit()
    for opt, arg in opts:
        if opt == "-t":
            # todo run test file or type checker
            sys.exit()
        elif opt == '-h':
            browser.headless(chromedriverPath)
        elif opt == '-r':
            browser.remote(currentSessionPath)
            login_req = False
        elif opt == '-m':
            login_req = False
            manual_login = True
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-w", "--gameworld"):
            world = arg

    if browser.driver == None:
        browser.chrome(chromedriverPath)

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

        login(browser=browser, gameworld=world, email=email, password=password)

        # clear loging credentials
        email = None
        password = None

    if manual_login:
        browser.use()
        browser.get('https://kingdoms.com')
        time.sleep(120)
        browser.done()

    game = gameworld(browser, world)

    # actions the bot will do

    # game.enableAdventures() #auto starting adventures if possible
    # first param = village index second param = building slot id
    #game.upgradeSlot(0, 1)

    # village, farmlist, interval in seconds
    #game.startFarming(0, [0], 400)
    #game.sortDangerFarms(farmlists=[0], toList=1, yellow=False, red=True)


    # path to farmlist file - farms without travian plus
    # game.startFarmlist("./assets/farmlist.txt")
from collections import namedtuple


def test(struct):
    print(struct.a)
    struct.a = 59


if __name__ == "__main__":
    struct = namedtuple("struct", "a b c")
    m = struct(23, 10, None)
    test(m)
    print(m.a)

from src import client, account, gameworld
import sys

# settings
chromedriverPath = './assets/chromedriver'
world = 'COM4'  # choose uppercase (exact world name)

# settings path
credentialsPath = "./assets/credentials.txt"
currentSessionPath = './assets/currentSession.txt'

# read login credentials
file = open(credentialsPath, "r")
text = file.read()
file.close()

email = text.split(";")[0]
password = text.split(";")[1]

browser = client()

# get startup arguments
if len(sys.argv) > 1 and sys.argv[1] == "-r":
    filename = currentSessionPath
    browser.remote(filename)
elif len(sys.argv) > 1 and sys.argv[1] == "-h":
    browser.headless(chromedriverPath)
    acc = account(browser, email, password)
    acc.login(world)
elif len(sys.argv) > 1 and sys.argv[1] == "-t":
    exit
else:
    browser.chrome(chromedriverPath)
    acc = account(browser, email, password)
    acc.login(world)


game = gameworld(browser, world)

# actions the bot will do

# game.enableAdventures() #auto starting adventures if possible
# first param = village index second param = building slot id
game.upgradeSlot(0, 1)

# village, farmlist, interval in seconds
game.startFarming(0, [1], 60)

from customDriver import client
from account import account
from gameworld import gameworld, village
import sys

# read login credentials
file = open("credentials.txt", "r")
text = file.read()
file.close()

email = text.split(";")[0]
password = text.split(";")[1]

# choose uppercase (exact world name)
world = 'COM4'

browser = client()

if len(sys.argv) > 1 and sys.argv[1] == "-r":
    filename = './currentSession.txt'
    browser.remote(filename)
elif len(sys.argv) > 1 and sys.argv[1] == "-h":
    browser.headless('./chromedriver')
    acc = account(browser, email, password)
    acc.login(world)
else:
    browser.chrome('./chromedriver')
    acc = account(browser, email, password)
    acc.login(world)

game = gameworld(browser, world)

# game.enableAdventures() #auto starting adventures if possible
# first param = village index second param = building slot id
game.upgradeSlot(0, 1)
game.upgradeSlot(0, 2)

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
else:
    browser.chrome('./chromedriver')
    acc = account(browser, email, password)
    acc.login(world)

game = gameworld(browser, world)

game.enableAdventures()
#vil = village(browser)
# vil.upgrade(2)

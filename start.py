from src import king_bot
import sys

# these could be read in via arguments, file or login manually - read documentation
gameworld = ""  # choose uppercase (exact world name) - optional
email = ""  # optional
password = ""  # optional
proxy = ""  # optional

# without extension (even on windows)
chrome_driver_path = './assets/chromedriver'

kingbot = king_bot(email=email, password=password, gameworld=gameworld,
                   chrome_driver_path=chrome_driver_path, proxy=proxy, start_args=sys.argv)

# place your actions below

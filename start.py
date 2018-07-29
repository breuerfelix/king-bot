from src import king_bot
import sys

# these could be read in via arguments, file or login manually - read documentation
gameworld = ""  # choose uppercase (exact world name) - optional
email = ""  # optional
password = ""  # optional
proxy = ""  # optional

kingbot = king_bot(email=email, password=password,
                   gameworld=gameworld, proxy=proxy, start_args=sys.argv)

# place your actions below

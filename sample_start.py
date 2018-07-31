from src import king_bot
import sys


gameworld = 'COM5'  # choose uppercase (exact world name) - optional
email = 'test@gmail.com'  # optional
password = 'save_password4000'  # optional
proxy = ''  # optional

# without extension (even on windows)
chrome_driver_path = './assets/chromedriver'

kingbot = king_bot(email=email, password=password, gameworld=gameworld,
                   chrome_driver_path=chrome_driver_path, proxy=proxy, start_args=sys.argv, debug=False)

kingbot.start_adventures(interval=500)

kingbot.start_farming(village=0, farmlists=[0], interval=120)

kingbot.start_custom_farmlist(path="./assets/farmlist.txt")

kingbot.sort_danger_farms(
    farmlists=[0], to_list=1, red=True, yellow=False, interval=240)

kingbot.dodge_attack(village=0, units=[1, 2, 11], target=[-10, 53])
kingbot.dodge_attack(village=1, units=[-1], target=[-20, 60])

kingbot.upgrade_units_smithy(village=0, units=[21, 25, 23])

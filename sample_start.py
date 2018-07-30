from src import king_bot, settings
import sys


gameworld = 'COM5'  # choose uppercase (exact world name) - optional
email = 'test@gmail.com'  # optional
password = 'save_password4000'  # optional
proxy = ''  # optional
settings.browser_speed = 1.0  # increase the number if your internet connecion is slow

kingbot = king_bot(email=email, password=password, gameworld=gameworld,
                   proxy=proxy, start_args=sys.argv, debug=False)

kingbot.start_adventures(interval=500)

kingbot.start_farming(village=0, farmlists=[0], interval=120)

kingbot.start_custom_farmlist()

kingbot.sort_danger_farms(
    farmlists=[0], to_list=1, red=True, yellow=False, interval=240)

kingbot.dodge_attack(village=0, units=[1, 2, 11], target=[-10, 53])
kingbot.dodge_attack(village=1, units=[-1], target=[-20, 60])

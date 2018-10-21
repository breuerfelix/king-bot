from src import king_bot, settings
import sys


gameworld = 'COMX'  # choose uppercase (exact world name) - optional
email = 'test@gmail.com'  # optional
password = 'save_password4000'  # optional
proxy = ''  # optional
settings.browser_speed = 1.0  # increase the number if your internet connecion is slow

kingbot = king_bot(email=email, password=password, gameworld=gameworld,
                   proxy=proxy, start_args=sys.argv, debug=False)

kingbot.start_adventures(interval=500, health=35)

kingbot.start_farming(village=0, farmlists=[0], interval=120)

kingbot.start_custom_farmlist()

kingbot.celebrate(villages=[0, 2, 3])

kingbot.sort_danger_farms(
    farmlists=[0], to_list=1, red=True, yellow=False, interval=240)

kingbot.dodge_attack(village=0, units=[1, 2, 11], target=[-10, 53])
kingbot.dodge_attack(village=1, units=[-1], target=[34, 9], save_resources=True, units_train=[1, 5])

kingbot.upgrade_units_smithy(village=0, units=[21, 25, 23])

kingbot.start_building(village=2, file_name='village_2.json')

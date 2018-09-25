# king-bot <!-- omit in toc -->

check out the insights of this project: [scriptworld.net](https://scriptworld.net/projects/king-bot/)

feel free to join the [official discord channel](https://discord.gg/5n2btF7) or **[contact me! (:](mailto:f.breuer@scriptworld.net)**

you want to run the bot **24/7**, but don't want to use your computer? **[contact me aswell! (:](mailto:f.breuer@scriptworld.net)**

__youtube video:__ how to setup the bot. [click here !](https://youtu.be/JGqBnTLFDFc)

[![Build Status](https://travis-ci.org/scriptworld-git/king-bot.svg?branch=master)](https://travis-ci.org/scriptworld-git/king-bot)
[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/scriptworld-git/king-bot/blob/master/LICENSE)
[![built with Selenium](https://img.shields.io/badge/built%20with-Selenium-yellow.svg)](https://github.com/SeleniumHQ/selenium)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)

# table of contents <!-- omit in toc -->

- [getting-started](#getting-started)
- [features](#features)
    - [farming (travian plus)](#farming-travian-plus)
    - [sorting out yellow / red farms](#sorting-out-yellow--red-farms)
    - [farmlists as .txt file (no travian plus needed)](#farmlists-as-txt-file-no-travian-plus-needed)
    - [adventures](#adventures)
    - [dodge incoming attacks](#dodge-incoming-attacks)
    - [upgrade units in smithy](#upgrade-units-in-smithy)
    - [upgrade resource fields / buildings](#upgrade-resource-fields--buildings)
- [start options](#start-options)
    - [provide credentials](#provide-credentials)
    - [headless browsing](#headless-browsing)
    - [login manually](#login-manually)
    - [remote browser](#remote-browser)
    - [proxy](#proxy)
- [faq](#faq)
- [how to contribute](#how-to-contribute)
    - [code style](#code-style)
    - [workflow](#workflow)
    - [nice to know](#nice-to-know)
    - [changelog](#changelog)
- [contact](#contact)

# getting-started

watch the youtube video if you got problems setting up the bot. [click here !](https://youtu.be/JGqBnTLFDFc)

1.  install python3 for your system
    1.  [get python](https://www.python.org/downloads/)
    2.  you need version 3.7 or higher
2.  clone this repository
3.  install packages
    1.  open console
    2.  goto this repository
    3.  run `pip install .` or `pip install -r requirements.txt`
4.  download chromedriver for your system _(optional)_
    1.  [get chromederiver](http://chromedriver.chromium.org)
    2.  move to `assets/` folder
5.  edit `start.py`
    1.  insert your credentials _(optional)_
        1.  login without inserting -> _see chapter start options_
    2.  place the actions your bot should do at the end
        1.  read documentation for this
        2.  read `sample_start.py` to get an impression
7.  execute script
    1.  `python start.py`
    2.  read documentation for options like remote browser or headless browsing
8.  on mac or linux
    1.  use `python3` and `pip3` instead

# features

just an overview with method signatures. for details check each chapter.

```python
def start_adventures(interval: int = 100, health: int = 50) -> None:
def start_farming(village: int, farmlists: list, interval: int) -> None:
def start_custom_farmlist(reload: bool = False) -> None:
def sort_danger_farms(farmlists: list, to_list: int, red: bool, yellow: bool, interval: int = 300) -> None:
def dodge_attack(village: int, interval: int = 600, units: list = [], target: list = []) -> None:
def upgrade_units_smithy(village: int, units: list, interval: int = 1000) -> None:
```

## farming (travian plus)

the bot will open given village, selects all farmlists from the array, sends them, and go to sleep.  
this is by far the simplest implementation of a farm bot.

```python
# sends farmlist with index 1 (the one after the starter list)
# in your first village (index 0) in an interval of 60 seconds
kingbot.start_farming(village=0, farmlists=[1], interval=60)

#sends farmlist 1 and 3 in your second village in an interval of 30 seconds
kingbot.start_farming(1, [1,3], 30)
```

**village:**  
index of village _(0 is the first village)_

**farmlists:**  
index of farmlist _(0 is the starter list with only 10 farms)_  
must be an _array_! you can send multiple lists in this interval

**interval:**  
interval of sending the list _in seconds_

you can stack as many of them together if you want.  
it's also possible to send different farmlist in the same village in different intervals.

## sorting out yellow / red farms

**note that this feature is not fully tested yet!**  
_i need someone with alot of big farmlists to test this feature for me_

this line will let the bot automaticly sort out red or/and yellow farms for you.  
it is checking all given farmlists in an interval (_in seconds_) for danger farms.  
if a farm is yellow or red, and you set the equivalent value to `True`, this farm will be placed onto the farmlist with the index given by the paramter `to_list`.  
the starter farmlist is index 0.

```python
kingbot.sort_danger_farms(farmlists=[0], to_list=1, red=True, yellow=False, interval=240)
```

**farmlists:**  
array of farmlist indexes _(start farmlist is 0)_

**to_list:**  
index of the farmlist the 'danger' farms will be put into  
`-1` if you want the farm to be removed instead of moved to another list

**red:**  
`True` if you want red farms to be sorted out

**yellow:**  
`True` if you want also yellow farms to be sorted out

**interval:**  
interval of checking the farmlists _in seconds_

## farmlists as .txt file (no travian plus needed)

this technique is a little bit slower than then one with travian plus.  
the bot will manually launch every attack at the rally point.  
i only implemented this feature for people who doesn't want to pay for the game and still want to farm only around 200 villages.

you have to create a file named `farmlist.txt` in `assets/` folder, which looks like the following: _(attention for separators!)_

```csv
-26;-34;120;0;1,2
-28;-24;70;0;1,2,3,4
-30;-57;300;0;1,2
```

**pattern:**  
x-coordinate **;** y-coordinate **;** time to wait till sending the troops again in seconds **;** index of village **;** index of unit in the horizontal bar **,** amount of units

every line represents one farm. the first 2 values are the x- and y-coordinates.  
the third value is the time _(in seconds)_ the bot waits until it sends the farm again.  
fourth value is the village from where the troops are going to be send off.  
the last values _(comma separated!)_ are the amount and index of the unit which is going to be send.  
you can find out the index when trying to launch a new attack. you will be asked which village you want to attack and which troops you wanna use.  
from left to right, starting at 0, these are the indexes of the units you want to use.  
for example _(gauls)_: 0 = phalanx, 1 = swordsman.  
if you want to send different units, just stack them at the end.  
...0,1,3,4 -> this would send 1 of unit 0 and 4 of unit 3 to this farm.

**attention:**  
_adding a unit index of `-1` will send **all** units with max number to this farm._  
_adding a unit value of `-1` will send **all** units of this type to this farm._

add the following line to your `start.py` script:

```python
kingbot.start_custom_farmlist(reload=False)
```

__reload:__  
if you set this value to `True` the bot will rescan your farmlist file every minute for changing lines  
you can add or remove farms without restarting the script

## adventures

this enables auto sending the hero on adventures.  
you hero won't die, because they will only start when the hero is above x hp.

```python
kingbot.start_adventures(interval=500, health=35)
```

**interval:** _(optional -> default = 100)_  
time _in seconds_ the hero thread will sleep until it checks for a new adventure again

**health:** _(optional -> default = 50)_  
minimum health _(in percent)_ of hero to start an adventure

## dodge incoming attacks

since everybody hates to get attacked at night, the bot is able do dodge incoming attacks.  
it will send your units to a given village for raid. make sure the village is inactive and valid.

the bot will wake up 10 minutes before the attack lands, so take a target which is at least 5:01 minutes away. (7:00 if you got a map and also send your hero)  
use this method for every village you want to save.

```python
kingbot.dodge_attack(village=0, units=[1, 0, 3], target=[1, 1])
```

**village:**  
index of village which the bot is going to check _(starting at 0)_

**units:**  
array of unit indexes which are going to be saved _(starting at 0)_  
insert `-1` _(units=[-1])_ to save **all** available units in this village

**target:**  
first index is the x-coordinate and second for the y-coordinate of the village the bot will send the units for a robbery

## upgrade units in smithy

```python
kingbot.upgrade_units_smithy(village=0, units=[21, 22])
```
__village:__  
index of village _(starting at 0)_

__units:__  
list of units you want to upgrade   
first one with highest priority, last one with lowest  

| roman                  | teuton              | gaul                  |
| ---------------------- | ------------------- | --------------------- |
| 1: legionnaire         | 11: clubswinger     | 21: phalanx           |
| 2: praetorian          | 12: spearfighter    | 22: swordsman         |
| 3: imperian            | 13: axefighter      | 23: pathfinder        |
| 4: equites legati      | 14: scout           | 24: theutates thunder |
| 5: equites imperatoris | 15: paladin         | 25: druidrider        |
| 6: equites caesaris    | 16: teutonic knight | 26: headuan           |
| 7: battering ram       | 17: ram             | 27: ram               |
| 8: fire catapult       | 18: catapult        | 28: trebuchet         |
| 9: senator             | 19: chief           | 29: chieftain         |
| 10: settler            | 20: settler         | 30: settler           |

the bot checks if it can upgrade given units in given order. first it checks swordsman in this example and if they are not available or maxed out, it will try to upgrade phalax again.  
you can increase the list as long as you want to.

the bot can't switch smithy pages for now, so make sure the window is big enough to cover 8 slots.   
By default this should be the case, otherwise it will just cover the 4 slots on the front for now.

sleeping time will be the time the academy needs to finish the current research, so the bot won't wake up unnecessarily in the given interval.

## upgrade resource fields / buildings

**note:** _this feature is disabled right now, it needs improvement!_

this function will upgrade a resource field or building in any village.

on the picture below you can see all field slot id's.  
these stay the same no matter what kind of village you have (even in 15er crop villages).

```python
kingbot.upgrade_slot(village=0, slot=5)
```

**village:**  
index of the village the slot should be upgraded in _(starting at 0)_

**slot:**  
see the picture below to get the right slot for your field

![resource-fields](https://scriptworld.net/assets/king-bot/resourceFields.png)

# start options

just an overview. for details check each topic.

| short | long        | arguments      | description             |
| :---: | :---------: | :------------: | :---------------------: |
| -e    | --email     | your_email     | optional for login      |
| -p    | --password  | your_password  | optional for login      |
| -w    | --gameworld | your_gameworld | optional for login      |
| -m    | -           | -              | login manually          |
| -h    | -           | -              | no browser window       |
| -r    | -           | -              | connect to last session |

## provide credentials

```bash
$ python start.py -e email@test.de -p your_password -w your_gameworld
$ python start.py --email email@test.de --password your_password --gameworld your_gameworld
```

if you don't want to store your credentials into a file, just provide them via arguments like this.  
it's also possible to login manually if you dont want to provide your login credentials at all. _see below: login manually_

all of these options are optional, you can always provice some via code, and some via start options, that's up to you.

## headless browsing

```bash
$ python start.py -h
```

if you don't wont a browser window to pop up, or using the script on a dedicated server with no gui, it is possible to run the script in headless mode.  
the console window will inform you about important actions the bot will do.

## login manually

```bash
$ python start.py -m 120
```

if you don't trust my program, even if it' open source, you can login manually and don't even type your email or password anywhere in my script.  
the bot will open the main page of travian kingdoms.  
it will now wait _120 seconds (given time via argument)_ for you to log into your account.  
after you are logged in, just open the gameworld you want your bot to run in.  
if you are finished, just wait for the timer to end, so the bot can do its work.

**note:** _this is not possible in headless mode!_

## remote browser

```bash
$ python start.py -r
```

if the script exists because of an exception, it's possible to re-use the browser session so you don't have to go through the whole login process again.  
just don't exit the browser window and make sure to remove the functions in the script, which the bot already completed in last session.  

__note:__ _debug mode must be enabled!_

## proxy

```python
proxy = '127.0.0.1:1234'
```

if you want to surf the web via proxy, just insert it in `start.py`. this is also possible in headless mode.  
if the proxy is set to `''`, it's going to be disabled. it's also disabled by default.

# faq

**can i play the game while the bot is running?**  
yes. just open a new browser window and leave the bot window in the background. login to your gameworld and keep playing.  
one instance doesn't effect another browser instance. you can also start your script without a browser window.

**can i get banned for using the bot?**  
yes, but the chances are below 1%. it's nearly impossible to detect this bot, because it clicks all buttons just like a human would do.  
also there is browser and sleeping time delay, so they can't event check if the interval is always the same.

__my internet is really slow. the bot is too fast and can't find elements!__  
`settings.browser_speed = 1.0` -> just increase this value. it will adjust __all__ sleep timers.  
you will find that value in `start.py` file.

# how to contribute

you are not quite sure if you are able to contribute ? **[contact me (: !](mailto:f.breuer@scriptworld.net)**  
i love to teach people who are interested in learning.

## code style

-   type definitions at least for method signatures
-   do comments
-   keep your code seperated in files

## workflow

-   take an issue or a personal idea to implement
-   fork the repository
-   start scripting
-   make a pull request

## nice to know

- store your login credentials in `./assets/credentials.txt` -> ignored by git
    - gameworld;your_email;your_password
- write your testscript as `test_start.py` -> ignored by git
- run mypy for typechecking `mypy start.py --ignore-missing-imports`
- set debug flag to `True` -> `kingbot = kingbot(..., debug=True)`
    - if your script executes with and error resume your session with `python start.py -r`

## changelog

[view changelog](CHANGELOG.md)

# contact

__discord:__ _scriptworld#9641_  
__email:__ _felix@scriptworld.net_

---

_we love lowercase_

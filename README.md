# king-bot

check out the insights of this project: [scriptworld.net](https://scriptworld.net/projects/king-bot/)

feel free to join the project or **[contact me! (:](mailto:f.breuer@scriptworld.net)**

you want to run the bot **24/7**, but don't want to use your computer? **[contact me aswell! (:](mailto:f.breuer@scriptworld.net)**

[![Build Status](https://travis-ci.org/scriptworld-git/king-bot.svg?branch=master)](https://travis-ci.org/scriptworld-git/king-bot)
[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/scriptworld-git/king-bot/blob/master/LICENSE)
[![built with Selenium](https://img.shields.io/badge/built%20with-Selenium-yellow.svg)](https://github.com/SeleniumHQ/selenium)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)

# installation

1.  install python3 for your system
    1.  [get python](https://www.python.org/downloads/)
2.  clone this repository
3.  install packages
    1.  open console
    2.  goto this repository
    3.  run `pip3 install .` or `pip3 install -r requirements.txt`
4.  download chromedriver for your system
    1.  [get chromederiver](http://chromedriver.chromium.org)
    2.  move to `assets/` folder
    3.  edit chromedriver path in `start.py` line 7 _(optinal)_
        1.  `chromedriverPath = 'enter path here'`
5.  store your login credentials _(optional)_
    1.  **you don't want to store them into a file? or login manually?**
        1.  _see chapter start options!_
    2.  create file named `credentials.txt` in `assets/` folder
    3.  write your email and password like following
    4.  `test@gmail.com;my_password`
    5.  save the file
6.  edit `start.py`
    1.  edit your gameworld in line 8 `world = 'COM4'`
        1.  make sure to use uppercase!
        2.  you can also provide the world via argument - see chapter start options
    2.  place the actions your bot have to do at the end
        1.  read documentation for this
7.  execute in console:
    1.  `python3 start.py`
    2.  read documentation for options like remote browser or headless browsing

# documentation

the first code snippet in each section always shows some example implementation of the action you want to perform.

## specify the bot

### farming (travian plus)

```python
# sends farmlist with index 1 (the one after the starter list)
# in your first village (index 0) in an interval of 60 seconds
game.startFarming(village=0, farmlists=[1], interval=60)

#sends farmlist 1 and 3 in your second village in an interval of 30 seconds
game.startFarming(1, [1,3], 30)
```

**first param:**  
index of village (0 is the first village)

**second param:**  
index of farmlist (0 is the starter list with only 10 farms)  
must be an _array_! you can send multiple lists in this interval

**third param:**  
interval of sending the list _in seconds_

you can stack as many of them together if you want.  
it's also possible to send different farmlist in the same village in different intervals.

### sorting out yellow / red farms

**note that this feature is not fully tested yet!**  
_i need someone with alot of big farmlists to test this feature for me_

this line will let the bot automaticly sort out red or/and yellow farms for you.  
it is checking all given farmlists in an interval (_in seconds_) for danger farms.  
if a farm is yellow or red, and you set the equivalent value to `True`, this farm will be placed onto the farmlist with the index given by the paramter `toList`.  
the starter farmlist is index 0.

```python
game.sortDangerFarms(farmlists=[0], toList=1, yellow=False, red=True, interval=240)
```

**first param:**  
array of farmlist indexes (start farmlist is 0)

**second param:**  
index of the farmlist the 'danger' farms will be put into

**third param:**  
`True` if you want yellow farms to be sorted out

**fourth param:**  
`True` if you want also red farms to be sorted out

**fifth param:**  
interval of checking the farmlists _in seconds_

### farmlists as .txt file (no travian plus needed)

this technique is a little bit slower than then one with travian plus.  
the bot will manually launch every attack at the rally point.  
i only implemented this feature for people who doesn't want to pay for the game and still want to farm only around 200 villages.

you have to create a file which looks like the following: (_attention for separators!_)

```csv
-26;-34;120;0;1,2
-28;-24;70;0;1,2
-30;-57;300;0;1,2
```

**pattern:** x-coordinate **;** y-coordinate **;** time to wait till sending the troops again in seconds **;** index of village **;** index of unit in the horizontal bar **,** amount of units

every line represents one farm. the first 2 values are the x- and y-coordinates.  
the third value is the time (_in seconds_) the bot waits until it sends the farm again.  
fourth value is the village from where the troops are going to be send off.  
the last values (_comma separated!_) are the amount and index of the unit which is going to be send.  
you can find out the index when trying to launch a new attack. you will be asked which village you want to attack and which troops you wanna use.  
from left to right, starting at 0, these are the indexes of the units you want to use.  
for example (gauls): 0 = phalanx, 1 = swordsman.

add the following line to your `start.py` script: (adjust the path to your .txt file if needed)

```python
# path to farmlist file - farms without travian plus
game.startFarmlist(path="./assets/farmlist.txt")
```

### adventures

```python
game.enableAdventures()
```

this enables auto sending the hero on adventures.  
be careful if the hero in low on health! there is no stopping mechanism for now.

### upgrade resource fields

```python
game.upgradeSlot(village=0, slot=5, amount=1)
```

this function will upgrade the resource field with id 5 for one level in your first village.  
increasing the amount parameter will increase the levels the building is getting upgraded.

on the picture below you can see all field id's.  
these stay the same no matter what kind of village you have (even in 15er crop villages).

![resource-fields](https://scriptworld.net/assets/king-bot/resourceFields.png)

## start options

### headless browsing

```bash
$ python3 start.py -h
```

if you don't wont a browser window to pop up, or using the script on a dedicated server with no gui, it is possible to run the script in headless mode.  
the console window will inform you about important actions the bot will do.

### provide credentials

```bash
$ python3 start.py -e email@test.de -p your_password
$ python3 start.py --email email@test.de --password your_password
```

if you don't want to store your credentials into a file, just provide them via arguments like this.  
it's also possible to login manually if you dont want to provide your login credentials at all.

### login manually

```bash
$ python3 start.py -m
```

if you don't trust my program, even if it' open source, you can login manually and don't even type your email or password anywhere in my script.  
the bot will open the main page of travian kingdoms.  
it will now wait _120 seconds_ for you to log into your account.  
after you are logged in, just open the gameworld you want your bot to run in.  
if you are finished, just wait for the timer to end, so the bot can do its work.

**note:** _this is not possible in headless mode!_

### remote browser

```bash
$ python3 start.py -r
```

if the script exists because of an exception, it's possible to re-use the browser session so you don't have to go through the whole login process again.  
just don't exit the browser window and make sure to remove the functions in the script, which the bot already completed in last session.

### proxy

```python
browser.chrome(chromedriverPath, proxy="127.0.0.1:1234")
```

if you want to surfe the web with a proxy, just provide it to the browser object. this is also possible in headless mode.  
if the proxy is set to `""`, it's going to be disabled. It's also disabled by default.

---

_i love lowercase_

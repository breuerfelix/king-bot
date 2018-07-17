# king-bot

check out the insights of this project: [scriptworld.net](https://scriptworld.net/projects/king-bot/)

feel free to join the project or **[contact me! (:](mailto:f.breuer@scriptworld.net)**

[![Build Status](https://travis-ci.org/scriptworld-git/king-bot.svg?branch=master)](https://travis-ci.org/scriptworld-git/king-bot)
[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/scriptworld-git/king-bot/blob/master/LICENSE)
[![built with Selenium](https://img.shields.io/badge/built%20with-Selenium-yellow.svg)](https://github.com/SeleniumHQ/selenium)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)

# installation

1.  install python3 for your system
    1.  [get python](https://www.python.org/downloads/)
2.  clone this repository
3.  install packages
    1.  open console as administrator
    2.  goto this repository
    3.  `python3 install.py`
4.  download chromedriver for your system
    1.  [get chromederiver](http://chromedriver.chromium.org)
    2.  move to `assets/` folder
    3.  edit chromedriver path in `start.py` line 7
        1.  `chromedriverPath = 'enter path here'`
5.  store your login credentials
    1.  create file named `credentials.txt` in `assets/` folder
    2.  write your email and password like following
    3.  `test@gmail.com;my_password`
    4.  save the file
6.  edit `start.py`
    1.  edit your gameworld in line 8 `world = 'COM4'`
        1.  make sure to use uppercase!
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
game.startFarming(0, [1], 60)

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
game.startFarmlist("./assets/farmlist.txt")
```

### adventures

```python
game.enableAdventures()
```

this enables auto sending the hero on adventures.  
be careful if the hero in low on health! there is no stopping mechanism for now.

### upgrade resource fields

```python
game.upgradeSlot(0, 5)
```

this function will upgrade the resource field with id 5 for one level in your first village.

on the picture below you can see all field id's.  
these stay the same no matter what kind of village you have (even in 15er crop villages).

![resource-fields](https://scriptworld.net/assets/king-bot/resourceFields.png)

## start options

### remote browser

```bash
$ python3 start.py -r
```

if the script exists because of an exception, it's possible to re-use the browser session so you don't have to go through the whole login process again.  
just don't exit the browser window and make sure to remove the functions in the script, which the bot already completed in last session.

### headless browsing

```bash
$ python3 start.py -h
```

if you don't wont a browser window to pop up, or using the script on a dedicated server with no gui, it is possible to run the script in headless mode.  
the console window will inform you about important actions the bot will do.

---

_i love lowercase_

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
    3.  edit chromedriver path in `start.py` _(optinal)_
        1.  `chrome_driver_path = 'enter path here'`
5.  edit `start.py`
    1.  place the actions your bot should do at the end
        1.  read documentation for this
        2.  read `sample_start.py` to get an impression
6.  insert your credentials _(optional)_
    1.  **you don't want to provide them? just login manually!**
        1.  _see chapter start options!_
    2.  create file named `credentials.txt` in `assets/` folder
    3.  write your email and password like following
    4.  `test@gmail.com;my_password`
    5.  save the file
7.  execute in console:
    1.  `python3 start.py`
    2.  read documentation for options like remote browser or headless browsing

# documentation

the first code snippet in each section always shows some example implementation of the action you want to perform.  
this snipped is followed by a short description for all parameters given to the method.

## specify the bot

### farming (travian plus)

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

### sorting out yellow / red farms

**note that this feature is not fully tested yet!**  
_i need someone with alot of big farmlists to test this feature for me_

this line will let the bot automaticly sort out red or/and yellow farms for you.  
it is checking all given farmlists in an interval (_in seconds_) for danger farms.  
if a farm is yellow or red, and you set the equivalent value to `True`, this farm will be placed onto the farmlist with the index given by the paramter `toList`.  
the starter farmlist is index 0.

```python
kingbot.sort_danger_farms(farmlists=[0], to_list=1, red=True, yellow=False, interval=240)
```

**farmlists:**  
array of farmlist indexes (start farmlist is 0)

**to_list:**  
index of the farmlist the 'danger' farms will be put into

**red:**  
`True` if you want red farms to be sorted out

**yellow:**  
`True` if you want also yellow farms to be sorted out

**interval:**  
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
kingbot.start_custom_farmlist(path="./assets/farmlist.txt")
```

**path:**  
path to your custom farmlist file

### adventures

this enables auto sending the hero on adventures.  
be careful if the hero in low on health! there is no stopping mechanism for now.

```python
kingbot.start_adventures(interval=500)
```

**interval:** _(optional -> default = 100)_  
time _in seconds_ the hero thread will sleep until it checks for a new adventure again

### upgrade resource fields / buildings

**note:** _this feature is disabled right now, it needs improvement!_

this function will upgrade a resource field or building in any village.

on the picture below you can see all field slot id's.  
these stay the same no matter what kind of village you have (even in 15er crop villages).

```python
kingbot.upgrade_slot(village=0, slot=5)
```

**village:**  
index of the village the slot should be upgraded in (starting at 0)

**slot:**  
see the picture below to get the right slot for your field

![resource-fields](https://scriptworld.net/assets/king-bot/resourceFields.png)

## start options

### provide credentials

```bash
$ python3 start.py -e email@test.de -p your_password -w your_gameworld
$ python3 start.py --email email@test.de --password your_password --gameworld your_gameworld
```

if you don't want to store your credentials into a file, just provide them via arguments like this.  
it's also possible to login manually if you dont want to provide your login credentials at all. _see below: login manually_  
all of these options are optional, you can always provice some via code, and some via start options, that's up to you

### headless browsing

```bash
$ python3 start.py -h
```

if you don't wont a browser window to pop up, or using the script on a dedicated server with no gui, it is possible to run the script in headless mode.  
the console window will inform you about important actions the bot will do.

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
proxy = '127.0.0.1:1234'
```

if you want to surf the web via proxy, just insert it in `start.py`. this is also possible in headless mode.  
if the proxy is set to `''`, it's going to be disabled. it's also disabled by default.

---

_i love lowercase_

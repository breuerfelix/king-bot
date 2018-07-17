import os


def install(package):
    os.system('pip3 install {}'.format(package))


install("schedule")
install("selenium")

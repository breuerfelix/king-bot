import os


def install(package):
    os.system('pip3 install {} --user'.format(package))


install("schedule")
install("selenium")
install("typing")

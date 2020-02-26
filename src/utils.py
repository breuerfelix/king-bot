import datetime
import time
import threading


def log(message: str):
    print_status(message)


def error(message: str):
    print_status(message, bcolors.FAIL, "ERROR")


def warning(message: str):
    print_status(message, bcolors.WARNING, "WARNING")


def info(message: str):
    print_status(message, bcolors.HEADER, "INFO")


def check_for_lines(path: str, current_lines: list) -> dict:
    lines_to_add: list = []
    lines_to_remove: list = []

    with open(path, "r") as file:
        lines = file.read().splitlines()

    for line in lines:
        if line not in current_lines:
            log("new line: " + str(line))
            lines_to_add.append(line)

    for job in current_lines:
        if job not in lines:
            log("removed / changed line: " + str(line))
            lines_to_remove.append(job)

    return {"add": lines_to_add, "remove": lines_to_remove}


def parse_time_to_seconds(time: str) -> int:
    """needs hour:minutes:seconds as paramter, returns time in seconds"""
    timelist = time.split(":")
    seconds = int(timelist[0]) * 60 * 60 + int(timelist[1]) * 60 + int(timelist[2])

    return seconds


def print_status(message: str = None, color: str = "\033[92m", status: str = "OK"):
    output = (
        "["
        + color
        + " "
        + status
        + " "
        + bcolors.ENDC
        + "] "
        + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
    )
    thread_name = threading.current_thread().name
    if thread_name is not None:
        output += " [" + bcolors.OKBLUE + thread_name + bcolors.ENDC + "]"
    if message is not None:
        output += " " + message
    print(output)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

    def disable(self):
        self.HEADER = ""
        self.OKBLUE = ""
        self.OKGREEN = ""
        self.WARNING = ""
        self.FAIL = ""
        self.ENDC = ""

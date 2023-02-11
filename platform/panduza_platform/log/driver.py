import re
import logging
from colorama import Fore, Back, Style

from .helpers import level_highlighter, re_highlighter, highlighter

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL


level_patterns = {
    "DEBUG": Fore.WHITE + Style.DIM,
    "INFO": Fore.BLUE + Style.NORMAL,
    # WARN=30.
    # ERROR=40.
    # CRITICAL=50.
}

re_patterns = [
    [ re.compile(r'[\s,]+(\d.+)[\s,]+'), Fore.CYAN], # numbers
    [ re.compile(r'\'.*?\''), Fore.YELLOW], # strings
    [ re.compile(r'\".*?\"'), Fore.YELLOW], # strings

    # @
    # #
    # |
    # |
]

patterns = {
    "\"name\"": Fore.GREEN,
    "\"group\"": Fore.GREEN,
    "\"driver\"": Fore.RED,
}


BACKS = [Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]


class DriverFormatter(logging.Formatter):

    NextBackId=0

    def __init__(self):
        super().__init__()
        self.back_id = DriverFormatter.NextBackId
        self.back = BACKS[self.back_id]
        DriverFormatter.NextBackId = (DriverFormatter.NextBackId+1)%len(BACKS)


    def formatMessage(self, record):

        # print(record.__dict__)
        # print(self.back_id)

        debug=""
        if record.levelname == "DEBUG":
            debug=Style.DIM

        hmsg = record.message
        hmsg = re_highlighter(hmsg, re_patterns, debug)
        hmsg = highlighter(hmsg, patterns, debug)
        
        output = ""
        # output += record.threadName + "."
        output += level_highlighter(record.levelname.ljust(8, ' '), level_patterns)
        output += "| "
        output += Style.BRIGHT + self.back + record.name + Style.RESET_ALL + "."
        output += debug + hmsg

        return output




def driver_logger(driver_name):

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(DriverFormatter())

    __logger = logging.getLogger(driver_name)
    __logger.setLevel(logging.DEBUG)
    __logger.addHandler(ch)

    return __logger



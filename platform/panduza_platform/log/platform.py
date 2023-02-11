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




class PlatformFormatter(logging.Formatter):
    def formatMessage(self, record):

        debug=""
        if record.levelname == "DEBUG":
            debug=Style.DIM

        hmsg = record.message
        hmsg = re_highlighter(hmsg, re_patterns, debug)
        hmsg = highlighter(hmsg, patterns, debug)
        
        output = ""
        output += level_highlighter(record.levelname.ljust(8, ' '), level_patterns)
        output += "| "
        output += debug + hmsg
            
        return output




def platform_logger():

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(PlatformFormatter())

    __logger = logging.getLogger("platform")
    __logger.setLevel(logging.DEBUG)
    __logger.addHandler(ch)

    return __logger



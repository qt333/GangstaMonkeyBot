import time
import datetime
import requests
import os
from bot.config import settings

TOKEN = settings.TG_BOT_TOKEN
CHAT_ID = settings.CHAT_ID

def tg_sendMsg(msg: str = "no message",TOKEN=TOKEN,chat_id=CHAT_ID,
    ps = "\n\n",
    *,
    sep_msg: bool = False,
):

    """send message via telegram api(url)\n
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    )"""
    # TOKEN = TOKEN
    # chat_id = chat_id
    _ps = ps
    isStr = type(msg) is str
    if isStr:
        msg = _ps + msg
    # if sep_msg and type(msg) == list:
    #     for m in msg:
    #         url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={m + _ps}"
    #         requests.get(url).json()
    # elif not sep_msg and type(msg) != str:
    #     msg = " \n".join([m for m in msg]) + _ps
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    )
    requests.get(url).json()

class Colors:
    # Source: https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

# class Time:
#     """Datetime | Timestamp \n
#     "06-10-2024 19:09:10"\n
#         1728230950"""
#     TIMESTAMP = int(time.time()) 
#     DATETIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

class Time:
    """Datetime | Timestamp \n
    "06-10-2024 19:09:10"\n
        1728230950"""
    
    @property
    def timestamp(self):
        return int(time.time())
    
    @property
    def datetime(self):
        return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")    
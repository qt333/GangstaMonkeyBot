import time
from bot.core.gangstamonkey import run_tapper
from threading import Thread
from bot.utils.scripts import get_session_names, get_users_data_names
from bot.utils.logger import logger
from bot.utils.utils import Colors

def start_threads():
    """Start sessions Threads"""

    sessions = get_session_names()
    sessions.remove('session_example')

    banner = """{}
   ____                       _        __  __             _              ____        _   
  / ___| __ _ _ __   __ _ ___| |_ __ _|  \/  | ___  _ __ | | _____ _   _| __ )  ___ | |_ 
 | |  _ / _` | '_ \ / _` / __| __/ _` | |\/| |/ _ \| '_ \| |/ / _ \ | | |  _ \ / _ \| __|
 | |_| | (_| | | | | (_| \__ \ || (_| | |  | | (_) | | | |   <  __/ |_| | |_) | (_) | |_ 
  \____|\__,_|_| |_|\__, |___/\__\__,_|_|  |_|\___/|_| |_|_|\_\___|\__, |____/ \___/ \__|
                    |___/                                          |___/                  
{}
""".format(Colors.GREEN , Colors.END)

    print(banner)
    print('{}Original{}: https://github.com/qt333/GangstaMonkeyBot'.format(Colors.GREEN, Colors.END))
    print('{}Donate here{} USDT/DOGS/HMSTR/NOT {}(TON){}: {}UQDyUVl29oSatC-oQeTYKb7gz6EljcmmUvzr2J0unEsP1o0c{}\n\n'.format(Colors.GREEN, Colors.END, Colors.LIGHT_CYAN, Colors.END, Colors.YELLOW, Colors.END))

    logger.info(f"Detected {len(sessions)} sessions")

    if len(sessions) == 0:
        logger.info('Sessions files not found. Before starting bot create your_session_name_here.json file in sessions/ folder.')
        return False

    threads_list = []

    for session in sessions:
        if session != "session_example":
            threads_list.append(Thread(target=run_tapper, args=(session,)))

    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()


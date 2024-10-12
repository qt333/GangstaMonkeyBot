from math import floor
import time
import random
from bot.utils.utils import tg_sendMsg, Colors
from bot.utils.logger import logger
from bot.api.auth import login
from bot.api.clicker import tap
from bot.config import settings
from bot.utils.json_db import JsonDB

#NOTE 
# add 1 intial tap before start main loop to parse income_per_tap available_taps taps_recover_per_sec data to session and then do main job
# add get_userdata() like it work in website? 
# add def calculate_clicks and write values to session.json


class Tapper:
    def __init__(self, session_name) -> None:
        self.session_name = session_name
        if settings.USE_RANDOM_DELAY_IN_RUN:
            self.startup_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
        else:
            self.startup_delay = 1
        self.token_updateAt = random.randint(settings.RANDOM_UPDATE_ACCESS_TOKEN[0], settings.RANDOM_UPDATE_ACCESS_TOKEN[1]) #token update on cycle
        self.counter = 0 #cycle counter

    def calculate_cooldown(self, user_data: dict) -> tuple:
        """Calculate cooldown_range for randomized start new cycle
        \n:data: dictionary resposne from request
        \n:return: tuple(value1,value2)
        \n\ncooldown = int((self.max_taps-self.available_taps)/self.taps_recover_per_sec)
        \ncooldown_range = (cooldown, cooldown + random.randint(30,65))"""
        # "available_taps": 140,
        # "max_taps": 5000,
        # "income_per_tap": 10,
        # "taps_recover_per_sec": 4,
        self.available_taps = user_data["available_taps"]
        self.max_taps = user_data["max_taps"]
        # income_per_tap = data["income_per_tap"]
        self.taps_recover_per_sec = user_data["taps_recover_per_sec"]
        
        cooldown = int((self.max_taps-self.available_taps)/self.taps_recover_per_sec)
        cooldown_range = (cooldown, cooldown + random.randint(settings.RANDOM_SLEEP_COOLDOWN_TAP[0], settings.RANDOM_SLEEP_COOLDOWN_TAP[1]))
        
        # print(f"\n {round(cooldown_range[0]/60,1)} minutes")
        return cooldown_range


    def calculate_clicks(self, user_data: dict):
        '''Calculate clicks_range'''

        self.available_taps = user_data["available_taps"]
        self.income_per_tap = user_data["income_per_tap"]
        clicks = floor(self.available_taps/self.income_per_tap) 
        clicks_range = [clicks - 15, clicks]
        db = JsonDB(self.session_name, path='sessions/')
        session_data = db.get_data()
        session_data['clicks_range'] = clicks_range
        db.save_data(session_data)

        return clicks_range

    def run(self):
        logger.info('{}{}{} | Thread has been started'.format(Colors.LIGHT_CYAN, self.session_name, Colors.END))
        time.sleep(self.startup_delay)
        try:
            session_data = login(self.session_name)
            if not session_data:
                return False
            initial_user_data = tap(self.session_name, zero_click=True)
            while 1:
                if self.counter == self.token_updateAt:
                    session_data = login(self.session_name)
                    self.counter = 0
                    if not session_data:
                        return False
                    initial_user_data = tap(self.session_name, zero_click=True)

                self.calculate_clicks(initial_user_data) #calc clicks and write values to sessin_data
                time.sleep(random.randint(45,86)) #delay to emulated time spend for clicks after login()
                user_data = tap(self.session_name)
                cooldown_range = self.calculate_cooldown(user_data)
                time.sleep(random.randint(cooldown_range[0],cooldown_range[1]))
                self.counter += 1

        except Exception as e:
            logger.error('{}{}{} | While running error occurs: {}'.format(Colors.LIGHT_CYAN, self.session_name, Colors.END, e))
            tg_sendMsg(f'{self.session_name} | While running error occurs: \n {e}', ps='[GangstaMonkey] Exception\n\n')
            return False
    
def run_tapper(session_name):
    try:
        Tapper(session_name).run()
    except Exception as e:
        logger.error(f'{session_name} | Error in "run_tapper": {e}')


        
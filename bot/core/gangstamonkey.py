from math import floor
import time
from datetime import datetime
import random
from bot.utils.utils import tg_sendMsg, Colors, Time
from bot.utils.logger import logger
from bot.api.auth import login
from bot.api.clicker import tap
from bot.api.daily_reward import claim_reward
from bot.config import settings
from bot.utils.json_db import JsonDB
from bot.api.boosts import run_boosters

#NOTE 
# add get_userdata() like it work in website? 

t = Time()

class Tapper:
    def __init__(self, session_name) -> None:
        self.session_name = session_name
        if settings.USE_RANDOM_DELAY_IN_RUN:
            self.startup_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
        else:
            self.startup_delay = 1
        self.token_updateAt = random.randint(settings.RANDOM_UPDATE_ACCESS_TOKEN[0], settings.RANDOM_UPDATE_ACCESS_TOKEN[1]) #token update on cycle
        self.counter = 0 #cycle counter
        self.next_boosters_use = 0

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
        self.max_taps = user_data["max_taps"]
        clicks = floor(self.available_taps/self.income_per_tap) 
        clicks_range = [clicks - 3, clicks]
        db = JsonDB(self.session_name, path='sessions/')
        session_data = db.get_data()
        session_data['clicks_range'] = clicks_range
        db.save_data(session_data)

        #calculate max clicks
        max_clicks = floor(self.max_taps/self.income_per_tap)
        max_clicks_range = [max_clicks - 3, max_clicks]
        return clicks_range, max_clicks_range

    def sleep_pattern(self):
        #NOTE EXPIREMENTAL FUNC, MAYBE IT WILL NOT WORK CAUSE OF UNABLE TO RECEIVE ACCESS TOKEN AFTER TIME.SLEEP(HOURS) ???
        if settings.USE_SLEEP_PATTERN:
            logger.info('{}{}{} | Going to sleep...'.format(Colors.LIGHT_CYAN, self.session_name, Colors.END))
            now = datetime.now()
            if now > settings.SLEEP_PATTERN_ACTIVATE_AFTER:
                time.sleep(settings.SLEEP_PATTERN_DURATION)
                logger.info('{}{}{} | Successfully waked up.'.format(Colors.LIGHT_CYAN, self.session_name, Colors.END))
                return True
            else: return False
        else:
            return False

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

                _, max_clicks_range = self.calculate_clicks(initial_user_data) #calc clicks and write values to sessin_data
                time.sleep(random.randint(45,86)) #delay to emulated time spend for clicks after login()
                user_data = tap(self.session_name)
                cooldown_range = self.calculate_cooldown(user_data)
                self.counter += 1

                # Boosters use logic
                if self.next_boosters_use:
                    use_boosters = t.timestamp > self.next_boosters_use
                if self.next_boosters_use == 0 or use_boosters:
                    run_boosters(self.session_name, max_clicks_range)
                    time.sleep(random.uniform(10,20))
                    
                    #claim daily reward
                    reward_data = claim_reward(self.session_name, 'GET')
                    if not reward_data['claimed_today'] and reward_data:
                        claim_reward(self.session_name, 'POST')
                    self.next_boosters_use = t.timestamp + 60*60*24
                if self.sleep_pattern():
                    continue
                time.sleep(random.randint(cooldown_range[0],cooldown_range[1]))

        except Exception as e:
            logger.error('{}{}{} | While running error occurs: {}'.format(Colors.LIGHT_CYAN, self.session_name, Colors.END, e))
            # tg_sendMsg(f'{self.session_name} | While running error occurs: \n {e}', ps='[GangstaMonkey] Exception\n\n')
            # return False
            raise
# @retry(
#     stop=stop_after_attempt(MAX_RETRIES),
#     wait=wait_fixed(RETRY_DELAY),
#     retry=retry_if_exception_type((NewConnectionError, SOCKSHTTPSConnectionPool)),  # Catch both exceptions
# )    
# def run_tapper(session_name):
#     try:
#         Tapper(session_name).run()
#     except Exception as e:
#         logger.error(f'{session_name} | Error in "run_tapper": {e}')

# Retry limit and delay between retries
MAX_RETRIES = 11
RETRY_DELAY = 180  # seconds

def run_tapper(session_name, attempt=1):
    try:
        # Attempt to run the session
        Tapper(session_name).run()
    except Exception as e:
        logger.error(f'{session_name} | Error in "run_tapper" on attempt {attempt}: {e}')
        if attempt < MAX_RETRIES:
            logger.info(f'{session_name} | Retrying №{attempt} in {RETRY_DELAY} seconds...')
            time.sleep(RETRY_DELAY)  # Optional: add delay before retrying
            run_tapper(session_name, attempt + 1)  # Recursive call to retry
            tg_sendMsg(f'{session_name} | While running run_tapper error occurs:\n {e}\n\nRetrying №{attempt} Successful!', ps='[GangstaMonkey] Exception run_tapper\n\n')
        else:
            logger.error(f'{session_name} | Max retries reached, giving up.')
        
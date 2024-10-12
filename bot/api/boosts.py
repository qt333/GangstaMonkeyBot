import requests
import random
import json
from bot.utils.logger import logger
from bot.utils.proxy import get_proxy_dict
from bot.utils.json_db import JsonDB
from bot.utils.utils import tg_sendMsg, Time
from bot.config import settings
from bot.utils.utils import Colors

tg = settings.TG_NOTIFICATIONS

def boosters_check(session_name: str) -> dict:
    """Check available boosters"""

    db = JsonDB(session_name, path='sessions/')
    session_data = db.get_data()

    userAgent = session_data["UserAgent"]
    proxy_string = session_data["proxy"]
    proxy = get_proxy_dict(proxy_string)
    access_token = session_data["access_token"]

    # tap url
    url = "https://gangsta-monkey.com/bringold-bot/backend/api/clicker/boosters/"

    headers = {
        "accept": "*/*",
        "accept-language": "ru,uk-UA;q=0.9,uk;q=0.8,en-US;q=0.7,en;q=0.6",
        "authorization": access_token,
        "cache-control": "no-cache",
        "content-type": "application/json",
        "UserAgent": userAgent,
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "Dnt":"1",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Origin": "https://gangsta-monkey.com",
        "Referer": "https://gangsta-monkey.com/bringold-bot/frontend/tap/boosters",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.get(url, headers=headers, proxies=proxy)
    boosters = response.json()
    # Checking the response
    if response.status_code == 200:
        full_energy = boosters["full_energy"]["slug"]
        full_energy_count = boosters["full_energy"]["available"]
        turbo = boosters["turbo"]["slug"]
        turbo_count = boosters["turbo"]["available"]
        
        boosters_data = {
            "full_energy":full_energy,
            "full_energy_count":full_energy_count,
            "turbo":turbo,
            "turbo_count":turbo_count
        }

        logger.info('{}{}{} | Check boosters | Full Energy: {}{}{} Turbo: {}{}{}'.format(
                Colors.LIGHT_CYAN, session_name, Colors.END, Colors.YELLOW, full_energy_count, Colors.END, Colors.YELLOW, turbo_count, Colors.END))
        # if tg:
        #     tg_sendMsg(f'{session_name} | Successful tap\nTotal Coins: {formatted_balance_coins}\n' \
        #         f'Available Taps: {formatted_available_taps}', ps='[GangstaMonkey]\n\n')
        return boosters_data
    else:
        # print("Failed to tap:", response.status_code, response.text)
        logger.info(f"{session_name} | Failed to get boosters: {response.status_code}, {response.text}")
        if tg:
            tg_sendMsg(f'{session_name} | Failed to get boosters: \n{response.status_code}, {response.text}', ps='[GangstaMonkey] Fail\n\n')
        return 0

def booster_activate(session_name, boost_slug):
    '''Activate boosters'''

    db = JsonDB(session_name, path='sessions/')
    session_data = db.get_data()

    telegram_id = session_data["telegram_id"]
    userAgent = session_data["UserAgent"]
    proxy_string = session_data["proxy"]
    proxy = get_proxy_dict(proxy_string)
    access_token = session_data["access_token"]

    # tap url
    url = "https://gangsta-monkey.com/bringold-bot/backend/api/clicker/boosters/activate/"

    payload = {"telegram_id":telegram_id,"slug":boost_slug}

    body = json.dumps(payload).encode('utf-8')  # Convert to bytes
    content_length = len(body)

    headers = {
        "accept": "*/*",
        "accept-language": "ru,uk-UA;q=0.9,uk;q=0.8,en-US;q=0.7,en;q=0.6",
        "authorization": access_token,
        "cache-control": "no-cache",
        "content-type": "application/json",
        "UserAgent": userAgent,
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "Dnt":"1",
        'Content-Length': str(content_length),
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Origin": "https://gangsta-monkey.com",
        "Referer": "https://gangsta-monkey.com/bringold-bot/frontend/tap/boosters",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.post(url, headers=headers, json=payload, proxies=proxy)
    boosters = response.json()
    # Checking the response
    if response.status_code == 200:
        full_energy = boosters["boosters"]["full_energy"]["slug"]
        full_energy_count = boosters["boosters"]["full_energy"]["available"]
        turbo = boosters["boosters"]["turbo"]["slug"]
        turbo_count = boosters["boosters"]["turbo"]["available"]
        
        boosters_data = {
            "full_energy":full_energy,
            "full_energy_count":full_energy_count,
            "turbo":turbo,
            "turbo_count":turbo_count
        }

        logger.success('{}{}{} | Successful booster activation | {}{}{}'.format(
                Colors.LIGHT_CYAN, session_name, Colors.END, Colors.YELLOW, boost_slug, Colors.END))
        # if tg:
        #     tg_sendMsg(f'{session_name} | Successful tap\nTotal Coins: {formatted_balance_coins}\n' \
        #         f'Available Taps: {formatted_available_taps}', ps='[GangstaMonkey]\n\n')
        return boosters_data
    else:
        # print("Failed to tap:", response.status_code, response.text)
        logger.info(f"{session_name} | Failed to activate booster: {response.status_code}, {response.text}")
        if tg:
            tg_sendMsg(f'{session_name} | Failed to activate booster: \n{response.status_code}, {response.text}', ps='[GangstaMonkey] Fail\n\n')
        return 0



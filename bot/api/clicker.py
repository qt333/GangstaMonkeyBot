import requests
import random
import json
from bot.utils.logger import logger
from bot.utils.proxy import get_proxy_dict
from bot.utils.json_db import JsonDB
from bot.config import settings
from bot.utils.utils import Colors, tg_sendMsg

tg = settings.TG_NOTIFICATIONS

def tap(session_name: str, zero_click = False) -> dict:
    """Send clicks\n
    :zero_click: if True, send clicks = 0 to get user_data\n
    :return: json response user_data\n\n
    {
    "telegram_id": 3453535,
    "username": "werwerwe",
    "first_name": "\ud83d\udc24 D345335a",
    "total_coins": 234341,
    "balance_coins": 266941,
    "ton_balance": 0.046,
    "level": 2,
    "available_taps": 0,
    "max_taps": 5000,
    "income_per_tap": 10,
    "taps_recover_per_sec": 4,
    "last_sync_update": 1728289450,
    "clan": "TON",
    "next_level_coins": 500000
}"""

    db = JsonDB(session_name, path='sessions/')
    session_data = db.get_data()

    telegram_id = session_data["telegram_id"]
    userAgent = session_data["UserAgent"]
    proxy_string = session_data["proxy"]
    # proxy = get_proxy_dict(proxy_string)
    proxy = {
        'https': proxy_string,
        'http': proxy_string
        }
    access_token = session_data["access_token"]
    click_range = session_data['clicks_range']
    # tap url
    url = "https://gangsta-monkey.com/bringold-bot/backend/api/clicker/tap/"

    if zero_click:
        clicks = 0 # for getting user_data
    else:
        clicks = random.randint(click_range[0], click_range[1])

    payload = {"telegram_id": telegram_id, "count": clicks}

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
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        'Content-Length': str(content_length),
        "Origin": "https://gangsta-monkey.com",
        "Referer": "https://gangsta-monkey.com/bringold-bot/frontend/start",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    # check_ip = requests.get('https://ipinfo.io', proxies=proxy)
    # proxy_data = check_ip.json()
    # logger.info(f'PRoxy: {proxy} | Current ip: {proxy_data["ip"]} | Current city: {proxy_data["city"]}')

    response = requests.post(url, headers=headers, json=payload, proxies=proxy)
    user_data = response.json()
    # Checking the response
    if response.status_code == 200:
        # print("Successful tap:", res)  # Or response.text for raw response
        if not zero_click:
            formatted_balance_coins = format(user_data["balance_coins"],",")
            formatted_available_taps = format(user_data["available_taps"],",")
            logger.success('{}{}{} | Successful tap | \nTotal Coins: {}{}{} Available Taps: {}{}{}'.format(
                Colors.LIGHT_CYAN, session_name, Colors.END, Colors.YELLOW, formatted_balance_coins, Colors.END, Colors.YELLOW, formatted_available_taps, Colors.END))
        if tg and not zero_click:
            tg_sendMsg(f'{session_name} | Successful tap\nTotal Coins: {formatted_balance_coins}\n' \
                f'Available Taps: {formatted_available_taps}', ps='[GangstaMonkey]\n\n')
        db = JsonDB(session_name, path='sessions/users_data/')
        db.save_data(user_data)
        return user_data
    else:
        # print("Failed to tap:", response.status_code, response.text)
        logger.info(f"{session_name} | Failed to tap: {response.status_code}, {response.text}")
        if tg:
            tg_sendMsg(f'{session_name} | Failed to tap: \n{response.status_code}, {response.text}', ps='[GangstaMonkey] Fail\n\n')
        return 0

def tap_clicks_range(session_name: str, clicks_range = [221,333]) -> dict:
    """Send certain clicks amount\n
    :clicks_range: list on range [175,275]
    \n
    :return: json response user_data\n\n
    {
    "telegram_id": 3453535,
    "username": "werwerwe",
    "first_name": "\ud83d\udc24 D345335a",
    "total_coins": 234341,
    "balance_coins": 266941,
    "ton_balance": 0.046,
    "level": 2,
    "available_taps": 0,
    "max_taps": 5000,
    "income_per_tap": 10,
    "taps_recover_per_sec": 4,
    "last_sync_update": 1728289450,
    "clan": "TON",
    "next_level_coins": 500000
}"""

    db = JsonDB(session_name, path='sessions/')
    session_data = db.get_data()

    telegram_id = session_data["telegram_id"]
    userAgent = session_data["UserAgent"]
    proxy_string = session_data["proxy"]
    proxy = get_proxy_dict(proxy_string)
    access_token = session_data["access_token"]
    # tap url
    url = "https://gangsta-monkey.com/bringold-bot/backend/api/clicker/tap/"

    click_range = clicks_range

    clicks = random.randint(click_range[0], click_range[1])

    payload = {"telegram_id": telegram_id, "count": clicks}

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
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        'Content-Length': str(content_length),
        "Origin": "https://gangsta-monkey.com",
        "Referer": "https://gangsta-monkey.com/bringold-bot/frontend/tap",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.post(url, headers=headers, json=payload, proxies=proxy)
    user_data = response.json()
    # Checking the response
    if response.status_code == 200:
        formatted_balance_coins = format(user_data["balance_coins"],",")
        formatted_available_taps = format(user_data["available_taps"],",")
        logger.success('{}{}{} | Booster tap | \nTotal Coins: {}{}{} Available Taps: {}{}{}'.format(
            Colors.LIGHT_CYAN, session_name, Colors.END, Colors.YELLOW, formatted_balance_coins, Colors.END, Colors.YELLOW, formatted_available_taps, Colors.END))
        # if tg:
        #     tg_sendMsg(f'{session_name} | Successful tap\nTotal Coins: {formatted_balance_coins}\n' \
        #         f'Available Taps: {formatted_available_taps}', ps='[GangstaMonkey]\n\n')
        # db = JsonDB(session_name, path='sessions/users_data/')
        # db.save_data(user_data)
        return user_data
    else:
        # print("Failed to tap:", response.status_code, response.text)
        logger.info(f"{session_name} | Failed to Booster tap: {response.status_code}, {response.text}")
        if tg:
            tg_sendMsg(f'{session_name} | Failed to Booster tap: \n{response.status_code}, {response.text}', ps='[GangstaMonkey] Fail\n\n')
        return 0
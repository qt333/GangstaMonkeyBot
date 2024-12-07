import requests
import random
import json
from bot.utils.logger import logger
from bot.utils.proxy import get_proxy_dict
from bot.utils.json_db import JsonDB
from bot.config import settings
from bot.utils.utils import Colors, tg_sendMsg

tg = settings.TG_NOTIFICATIONS

def claim_reward(session_name: str, method: str) -> dict:

    """Daily reward claim\n
    :method: 'GET' or 'POST'
    :return:     "last_claimed": 2,
    "claimed_today": true
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


    url = "https://gangsta-monkey.com/bringold-bot/backend/api/clicker/tasks/daily-reward/"

    payload = {}

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
        "Referer": "https://gangsta-monkey.com/bringold-bot/frontend/tasks/daily-rewards",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    if method == 'POST':
        response = requests.post(url, headers=headers, json=payload, proxies=proxy)
    else:
        response = requests.get(url, headers=headers, json=payload, proxies=proxy)
    reward_data = response.json()
    # Checking the response
    if response.status_code == 200 and method == 'POST':
        logger.success('{}{}{} | Successful claim Daily Reward\n Claimed:{}, LastClaimed:{}'.format(
            Colors.LIGHT_CYAN, session_name, Colors.END, reward_data["claimed_today"], reward_data["last_claimed"]))
        if tg:
            tg_sendMsg(f'{session_name} | Successful claim Daily Reward\n\n Claimed:{reward_data["claimed_today"]}, LastClaimed:{reward_data["last_claimed"]}', ps='[GangstaMonkey]\n\n')
        return reward_data
    elif response.status_code == 200 and method == 'GET':
        return reward_data
    else:
        # print("Failed to tap:", response.status_code, response.text)
        logger.info(f"{session_name} | Failed to claim Daily Reward: {response.status_code}, {response.text}")
        if tg:
            tg_sendMsg(f'{session_name} | Failed to claim Daily Reward: Method {method}\n{response.status_code}, {response.text}', ps='[GangstaMonkey] Fail\n\n')
        return 0

import requests
from bot.utils.logger import logger
from bot.utils.json_db import JsonDB
from bot.utils.proxy import get_proxy_dict
from bot.utils.utils import tg_sendMsg, Time, Colors
from bot.config import settings
import json

#TODO add content length and Origin:https://gangsta-monkey.com to headers

tg = settings.TG_NOTIFICATIONS

def login(session_name: str) -> dict:
    """Update token\n
    :tg: turn on tg notification\n
    :return: session data\n\n
    {
    "init_data": "sdfsdfsdf",
    "telegram_id": 45645656,
    "access_token": "dfgdfgdfgdfgdfgdfgdfghh-d1oEaQIwRA",
    "access_token_refreshTime": 20,
    "UserAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "proxy":"",
    "clicks_range": [
        493,
        500
    ],
    "lastUpdated": [
        "07-10-2024 08:32:12",
        1728279132
    ]
}"""
    t = Time()
    ts = t.timestamp
    dt = t.datetime

    db = JsonDB(session_name, path='sessions/')
    session_data = db.get_data()

    access_token = session_data["access_token"]
    init_data = session_data["init_data"]
    telegram_id = session_data["telegram_id"]
    referrer = session_data["referrer"]
    userAgent = session_data["UserAgent"]
    proxy_string = session_data["proxy"]
    proxy = get_proxy_dict(proxy_string)

    # token only for 12h probaply
    url = "https://gangsta-monkey.com/bringold-bot/backend/api/auth/login/"

    payload = {
        "init_data": init_data,
        "referrer": referrer
    }

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
        "Referer": "https://gangsta-monkey.com/bringold-bot/frontend",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    response = requests.post(url, headers=headers, json=payload, proxies=proxy)
    res = response.json()
    # Checking the response
    if response.status_code == 200:
        # print("Successfuly receive Access Token:", res)  # Or response.text for raw response
        # logger.info(f"{session_name} | Successfuly received Access Token: {res}")
        logger.info("{}{}{} | Successfuly received Access Token".format(Colors.LIGHT_CYAN, session_name, Colors.END))
        if tg and settings.TG_NOTIFICATIONS_ACCESS_TOKEN:
            tg_sendMsg(f'{session_name} | Successfuly receive Access Token', ps='[GangstaMonkey]\n\n')

        session_data["access_token"] = res['token']
        session_data["lastUpdated"] = [dt, ts]
        db.save_data(session_data)
        return session_data
    else:
        # print("Failed to reiceve Access Token:", response.status_code, response.text)
        logger.info('{}{}{} | Failed to reiceve Access Token: {}{}{}, {}{}{}'.format(Colors.LIGHT_CYAN, session_name, Colors.END, Colors.RED, response.status_code, Colors.END, Colors.LIGHT_PURPLE, response.text, Colors.END))
        if tg:
            tg_sendMsg(f'{session_name} | Failed to reiceve Access Token: \n{response.status_code}, {response.text}', ps='[GangstaMonkey] Failed\n\n')
            return 0
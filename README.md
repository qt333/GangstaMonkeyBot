[<img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue">](https://www.python.org/downloads/)

![demo](.github/images/demo.jpg)

## ⚡ Features
1. Support multi-sessions
2. Autotap when Enegry is full

## ⚙ [Settings](.env-example)
<details>
  <summary><b>TG_BOT_TOKEN / CHAT_ID / TG_NOTIFICATIONS </b> - Telegram data</summary>
  <p>These values are necessary if you wanna receive notification to Telegram.</p>
  <ul>
    <li><strong>Example:</strong></li>
    <code>CHAT_ID=2182472</code>
    <br>
    <code>TG_BOT_TOKEN=b592f0d605a1b67c20e8d1c7582f20</code>
    <br>
    <code>TG_NOTIFICATIONS=True</code>
    <br>
    <code>TG_NOTIFICATIONS_ACCESS_TOKEN=False</code>
  </ul>
</details>

<details>
  <summary><b>USE_RANDOM_DELAY_IN_RUN</b> - Use Random Delay at Startup</summary>
  <p>This setting allows for random delays for each session before starting the bot, helping to start each session separately rather than simultaneously.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>RANDOM_DELAY_IN_RUN</b> - Random Delay at Startup</summary>
  <p>Defines the range of random delay applied to each session before starting the bot. This helps to start each session separately rather than simultaneously.</p>
  <ul>
    <li><strong>Example:</strong> <code>[0, 120]</code></li>
    <li><strong>Default:</strong> <code>[0, 500]</code></li>
  </ul>
</details>

<details>
  <summary><b>RANDOM_UPDATE_ACCESS_TOKEN</b> - Access Token Update Frequency</summary>
  <p>Randomly choose how frequent Access Token will be updating depending of tap cycle count</p>
  <ul>
    <li><strong>Example:</strong> <code>[2, 4]</code></li>
    <li><strong>Default:</strong> <code>[2, 4]</code></li>
  </ul>
</details>


## 📕 [Session](sessions/session_example.json)
For each session, you should create a json file in `sessinos/` folder with your auth data (detailed instruction will be below in [Full Guide](docs/guide.md) how to get this data):
```json
{
  "init_data": "user=%7B%22first_name%22%3A%22%F0%9F%90%A4%22last_name%22%3A%22%22%2C%22username%22%3A%22%22%2C%22language_code%22%3A%22ru%22%7D&chat_instance=233190&chat_type=group&start_param=752&auth_date=1728501985&hash=6251751a478778e6c2dd",
  "telegram_id": 345683417,
  "referrer": "34583417",
  "access_token": "eyJhbGciOidfgdfgdfsDSF5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbretdGSRgdV9pZCI6NzUyNjgz9uIjoxNzI4NTIzNjM3LjIzMzI5MX0.mZ9Kl_H7WqKjFDghhsa5wesef",
  "UserAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
  "proxy": {},
  "clicks_range": [
    491,
    500
  ],
  "lastUpdated": [
    "08-10-2024 00:48:53",
    1728337733
  ]
}
```
> [!NOTE]
> `session_example` is example session names.  
> Not yet tested how quick `init_data` will be expired, so keep in mind that probably you will need to updated it sometimes (1 time a week?) with `access token` 


## ⚡ Quick Start
1. To install the libraries on Windows, run `INSTALL.bat` or `install.sh` on Linux.
2. To start the bot, use `START.bat` (or in the console: python main.py) if you use Windows or `start.sh` on Linux.


## 📌 Prerequisites
Before you start, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) version 3.10 or 3.11.


## 📃 Getting TG_BOT_TOKEN and CHAT_ID 
1. For `TG_BOT_TOKEN` api go to Telegram and get it from Bot Father. 
2. How to get `CHAT_ID` will be show in [Full Guide](docs/guide.md)  



## 🧱 Installation
You can clone the [**Repository**](https://github.com/qt333/GangstaMonkeyBot) to your system and installing the required dependencies:
```shell
~ >>> git clone https://github.com/qt333/GangstaMonkeyBot 
~ >>> cd GangstaMonkeyBot

# Linux
~/GangstaMonkeyBot >>> python3 -m venv venv
~/GangstaMonkeyBot >>> source venv/bin/activate
~/GangstaMonkeyBot >>> pip3 install -r requirements.txt
~/GangstaMonkeyBot >>> cp .env-example .env
~/GangstaMonkeyBot >>> nano .env  # Enter your TG_BOT_TOKEN and CHAT_ID
~/GangstaMonkeyBot >>> python3 main.py

# Windows
~/GangstaMonkeyBot >>> python -m venv venv
~/GangstaMonkeyBot >>> venv\Scripts\activate
~/GangstaMonkeyBot >>> pip install -r requirements.txt
~/GangstaMonkeyBot >>> copy .env-example .env
~/GangstaMonkeyBot >>> # Open the .env file and enter your TG_BOT_TOKEN and CHAT_ID
~/GangstaMonkeyBot >>> python main.py
```

> [!TIP]
> To install as a Linux service for background operation of the bot, see [here](docs/LINUX-SERVIS-INSTALL.md).

## Donation
    USDT/DOGS/HMSTR/NOT (TON): UQDyUVl29oSatC-oQeTYKb7gz6EljcmmUvzr2J0unEsP1o0c

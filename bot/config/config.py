from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Union, Dict, List, Optional, Tuple


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    TG_BOT_TOKEN: str = ""
    CHAT_ID: str = ""
    TG_NOTIFICATIONS: bool = True
    TG_NOTIFICATIONS_ACCESS_TOKEN: bool = False

    USE_RANDOM_DELAY_IN_RUN: bool = True
    RANDOM_DELAY_IN_RUN: List[int] = [0, 500] #seconds

    RANDOM_UPDATE_ACCESS_TOKEN:List[int] = [2, 4]

    RANDOM_SLEEP_COOLDOWN_TAP: List[int] = [25, 76] # additional sleep time in seconds for main Energy cooldown 
    
settings = Settings()
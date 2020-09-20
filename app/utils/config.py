import os
from typing import Any
from typing import Dict


class Global:
    CHECK_DATA: Dict[str, Any] = dict()           # the check data
    CHECK_DATA_FILE: str = 'data/checks.json'     # the file path stored check data
    CHECK_LOG_FILE: str = 'data/check_logs.csv'  # the file path stored check log
    DEFAULT_TIMEOUT: float = 3          # default timeout: 3 seconds
    DEFAULT_RESPONSE_TIME: float = 250  # default response time: 250 ms
    MONITOR_ON: bool = False            # the monitor is turn on/off


def get(key: str, default: Any = '') -> Any:
    """
    get one config value
    :param key: config key
    :param default: default value
    :return: config value
    """
    return os.getenv(key.upper(), default)


def get_bool(key: str) -> bool:
    """
    get bool config value
    :param key: config key
    :return: bool config
    """
    return str(os.getenv(key.upper())).upper() == 'TRUE'

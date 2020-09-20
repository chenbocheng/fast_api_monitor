from typing import Dict, List
from model.check import Check
from utils.logger import get_service_logger
from utils.config import Global
from utils.util import md5hash, jsondump, is_url
from datetime import datetime
from os import path
import json

LOGGER = get_service_logger('CHECK_SRV')


def save_item(check: Check) -> Dict:
    if len(Global.CHECK_DATA) > 100:
        raise Exception('The size of monitoring url has full. The size is %d now.' % len(Global.CHECK_DATA))

    # url is valid or not
    if not is_url(check.url):
        raise Exception('The url is invalid: %s' % check.url)

    key: str = md5hash(check.url)  # the data map key
    check.id = key
    check.created = datetime.now()
    Global.CHECK_DATA[key] = check.dict()
    save_all_to_data(Global.CHECK_DATA)
    return Global.CHECK_DATA[key]


def delete_item(check_id: str) -> bool:
    if check_id not in Global.CHECK_DATA.keys():
        return False
    del Global.CHECK_DATA[check_id]
    save_all_to_data(Global.CHECK_DATA)
    return True


def delete_all_items() -> bool:
    Global.CHECK_DATA = {}
    save_all_to_data(Global.CHECK_DATA)
    return True


def get_item(check_id: str) -> Dict:
    return Global.CHECK_DATA.get(check_id, None)


def get_items() -> List[Dict]:
    checks = []
    for key in Global.CHECK_DATA:
        checks.append(Global.CHECK_DATA[key])
    return checks


def load_checks() -> Dict:
    data = {}
    try:
        if path.exists(Global.CHECK_DATA_FILE):
            with open(Global.CHECK_DATA_FILE, 'r') as json_file:
                data = json.load(json_file)
    except IOError as ex:
        LOGGER.info('Read file %s error ' % Global.CHECK_DATA_FILE)
    finally:
        return data


def save_to_data(check: Dict) -> bool:
    """
    Save one check record to data file
    TODO: later into DB
    """
    json_text: str = jsondump(check)
    with open(Global.CHECK_DATA_FILE, 'a+') as json_file:
        json_file.writelines(json_text)
    return True


def save_all_to_data(check_map: Dict) -> Dict:
    """
    Save all check records to data file
    TODO: later into DB
    """
    json_text: str = jsondump(check_map)
    with open(Global.CHECK_DATA_FILE, 'w') as json_file:
        json_file.writelines(json_text)
    return check_map

from typing import Dict, List
from model.check import CheckLog, Status
from utils.logger import get_service_logger
from utils.util import jsondump
from utils.config import Global
from time import time
from aiohttp import ClientSession
import asyncio

LOGGER = get_service_logger('MONITOR_SRV')


def save_log_to_data(check_log: Dict) -> bool:
    """
    Save one check log to data file
    TODO: later into DB
    """
    json_text: str = jsondump(check_log)
    with open(Global.CHECK_LOG_FILE, 'a+') as json_file:
        json_file.writelines(check_log['id'] + ",\t"
                             + check_log['created'].isoformat() + ",\t"
                             + check_log['status'].name + ",\t"
                             + check_log['url'] + ",\t"
                             + str(round(check_log['time'])) + "\n")
    return True


async def async_get_url_status(url: str, timeout: float = Global.DEFAULT_TIMEOUT) -> CheckLog:
    """
    Check url and get status. Return a check log later on
    """
    check_log: CheckLog = CheckLog().create(url=url, status=Status.ERROR)

    async with ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout) as resp:
                start: float = time() * 1000
                await resp.text()
                elapsed = time() * 1000 - start
                check_log.time = elapsed
                if resp.status == 200:
                    LOGGER.info("Response %s: %f ms" % (url, elapsed))
                    if elapsed < Global.DEFAULT_RESPONSE_TIME:
                        check_log.status = Status.OK
                    else:
                        check_log.status = Status.SLOW
                else:
                    LOGGER.info('Response error: %s' % url)
                    check_log.status = Status.ERROR
        except asyncio.TimeoutError:
            check_log.status = Status.ERROR
            LOGGER.info('Response timeout: %s' % url)
        finally:
            save_log_to_data(check_log.dict())

    return check_log


async def async_check_urls(checks: List[Dict]):
    for check in checks:
        asyncio.create_task(async_get_url_status(check['url'], timeout=Global.DEFAULT_TIMEOUT))

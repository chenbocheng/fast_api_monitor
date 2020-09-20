from fastapi import FastAPI
from typing import List, Dict, Any
from utils import router, config, logger
from utils.config import Global
from service import check_service, monitor_service
from fastapi_utils.tasks import repeat_every

"""
USE os.getenv() TO GET ENV VARS IN dev.cfg OR prod.cfg
"""

env: str = config.get('ENV')
app_name: str = config.get('APP_NAME')
description: str = config.get('DESCRIPTION')
version: str = config.get('VERSION')
debug: bool = config.get_bool('DEBUG')

fastapi_cfg: Dict[str, Any] = {
    'debug': env != 'prod',
    'title': app_name,
    'description': description,
    'version': version,
    'is_debug': debug
}

# init app
app = FastAPI(**fastapi_cfg)
router.register_controllers(app)
router.register_middlewares(app)

LOGGER = logger.get_application_logger()


async def monitor_task():
    checks: List[Dict] = check_service.get_items()
    await monitor_service.async_check_urls(checks)
    Global.MONITOR_ON = True


@app.on_event('startup')
@repeat_every(seconds=60)
async def start_app():
    if not Global.MONITOR_ON:
        LOGGER.info('on_event startup: %s\n%s' % (app_name, fastapi_cfg))
        Global.CHECK_DATA = check_service.load_checks()
        LOGGER.debug('startup _CHECK_DATA: \n%s' % Global.CHECK_DATA)
        LOGGER.info('on_event startup END: %s' % app_name)

    LOGGER.debug('monitor_task call...')
    await monitor_task()


@app.on_event('shutdown')
async def shutdown_app():
    LOGGER.info('Shutdown application~')

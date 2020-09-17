from fastapi import FastAPI
from typing import Dict, Any

from utils import router, config, logger
from utils.config import Global
from service import check_service


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


@app.on_event('startup')
async def start_app():
    Global.CHECK_DATA = check_service.load_checks()
    LOGGER.info('startup _CHECK_DATA: \n%s' % Global.CHECK_DATA)
    LOGGER.info('Launching application: %s\n%s' % (app_name, fastapi_cfg))


@app.on_event('shutdown')
async def shutdown_app():
    LOGGER.info('Shutdown application~')

from fastapi import APIRouter
from utils.controller import success
from utils.logger import get_controller_logger
from utils import config
from utils.util import md5hash


app_name = config.get('APP_NAME')

router = APIRouter()

LOGGER = get_controller_logger('BASE')


@router.get('/ping')
def ping_check():
    return success(data={
        'name': app_name,
        'hash': md5hash(app_name),
    }, msg='OK')

from typing import List
from fastapi import APIRouter
from utils.controller import success, error
from utils.logger import get_controller_logger
from model.check import Check
from service import check_service


router = APIRouter()

LOGGER = get_controller_logger('CHECK')


@router.get('')
def get_checks():
    # get all check urls
    checks: List = check_service.get_items()
    return success(checks)


@router.post('', description='add/update a check')
def save_check(check: Check):
    try:
        check_saved = check_service.save_item(check)
        return success(check_saved)
    except Exception as ex:
        LOGGER.exception(ex)
        return error(msg=str(ex))


@router.delete('/{check_id}', description='delete a check')
def delete_check(check_id: str):
    if check_service.delete_item(check_id):
        return success(msg='Removed!')
    else:
        return error(msg='Cannot removed!')


@router.delete('', description='delete all checks')
def delete_checks():
    try:
        check_service.delete_all_items()
        return success(msg='ok')
    except Exception as ex:
        LOGGER.exception(ex)
        return error(msg=ex)

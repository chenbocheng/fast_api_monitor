from enum import Enum

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import uuid1


class Status(Enum):
    TODO = 0,
    OK = 1,
    SLOW = 2,
    ERROR = 3


class Check(BaseModel):
    """
    The url for monitor
    :param id: md5 of url
    :param url: the url address must contains http or https
    :param interval: the interval seconds
    :param created: 0 - ok, 1 - slow, 2 - error
    :param status: 0 - ok, 1 - slow, 2 - error
    """
    id: Optional[str] = None
    url: str
    interval: int = 60
    created: Optional[datetime] = None


class CheckLog(BaseModel):
    """
    The checking status logged every time
    :param url: the full url address contains http or https
    :param status: 0 - ok, 1 - slow, 2 - error
    :param time: Response time (ms)
    """
    id: Optional[str]
    url: Optional[str]
    created: Optional[datetime]
    status: Status = Status.OK
    time: int = 0

    def create(self, url, status=Status.ERROR):
        self.id = uuid1().hex
        self.url = url
        self.created = datetime.now()
        self.status = status
        self.time = 0
        return self

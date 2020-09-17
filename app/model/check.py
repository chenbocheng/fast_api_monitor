from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Check(BaseModel):
    """
    The url for monitor
    :param url: the url address must contains http or https
    :param interval: the interval seconds
    """
    id: Optional[str] = None
    url: str
    interval: int
    created: Optional[datetime] = None
    status: Optional[int] = 2


class CheckLogging(BaseModel):
    """
    The checking status logged every time
    :param url: the full url address contains http or https
    :param status: 0 - ok, 1 - slow, 2 - error
    """
    id: str
    url: str
    created: datetime
    status: int

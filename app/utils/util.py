from typing import Any
import hashlib
import json
from datetime import datetime, date


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.replace(microsecond=0).isoformat()
        elif isinstance(obj, date):
            return obj.replace(microsecond=0).isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


def jsondump(o: Any) -> str:
    """
    json dump object
    :return:
    """
    return json.dumps(o, indent=2, ensure_ascii=False, cls=JsonEncoder)


def md5hash(s: str, length: int = 16) -> str:
    """
    md5 hash
    :param s: string
    :param length: length (default is 8)
    :return: hashed string
    """
    if length <= 0 or length > 32:
        length = 16
    ret = hashlib.md5(s.encode()).hexdigest()
    if len(ret) > length:
        ret = ret[:length]
    return ret


def is_url(url: str) -> bool:
    return url.startswith(("http://", "https://"))

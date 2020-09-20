"""
test client, run it from root directory
python ./test/client.py
"""
import dotenv
import os
import sys

print(os.getcwd())
sys.path.insert(0, os.getcwd())

from model.check import Check
from utils.util import md5hash
from pprint import pprint

dotenv.load_dotenv('config/dev.cfg')
assert len(os.getenv('APP_NAME')) > 0

from app import app
from fastapi.testclient import TestClient

print(os.getcwd())
sys.path.insert(0, os.getcwd())
dotenv.load_dotenv('config/dev.cfg')
assert len(os.getenv('APP_NAME')) > 0

CHECK_ITEM = Check(
    url='https://www.google.com'
)


def test_save_check():
    client = TestClient(app)
    response = client.post('/checks', data=CHECK_ITEM.json())
    pprint(response.json())
    assert response.status_code == 200
    assert response.json()['data']['url'] == CHECK_ITEM.url
    assert response.json()['data']['id'] == md5hash(CHECK_ITEM.url)


def test_delete_check():
    client = TestClient(app)
    del_response = client.delete('/checks/' + md5hash(CHECK_ITEM.url))
    assert del_response.status_code == 200
    pprint(del_response.json())

    get_resp = client.get('/checks')
    pprint(get_resp.json()['data'])

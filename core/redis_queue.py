# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-06 16:04
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : redis.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import

# module level variables here

# Create your models here.
import json
from django.conf import settings
from django.test import TestCase

import redis

pool = redis.ConnectionPool(host=settings.REDIS["HOST"], port=settings.REDIS["PORT"])
r = redis.Redis(connection_pool=pool)

def push_download(data):
    global r
    if isinstance(data, dict):
        data = json.dumps(data)
    r.lpush(settings.REDIS["DOWNLOAD_KEY"],data)

def pop_download(timeout=None):
    global r
    key, ret_b = r.brpop(settings.REDIS["DOWNLOAD_KEY"], timeout)
    try:
        ret = json.loads(ret_b)
    except json.JSONDecodeError:
        print("json loads error:", ret_b)
        ret = {}
    return ret

def test_pop(a,b,c):
    data = {
      "songs": [
        {
          "name": "如果你也听说 (Live)",
          "id": 29005677,
          "pst": 0,
          "t": 0,
          "ar": [
            {
              "id": 10559,
              "name": "张惠妹",
              "tns": [],
              "alias": []
            }
          ],
          "alia": [],
          "pop": 95.0,
          "st": 0,
          "rt": None,
          "fee": 8,
          "v": 27,
          "crbt": None,
          "cf": "",
          "al": {
            "id": 2975319,
            "name": "STAR LIVE庆功演唱会",
            "picUrl": "https://p1.music.126.net/1Fg4WKSjj0dTSElhi_KFhg==/109951163244872785.jpg",
            "tns": [],
            "pic_str": "109951163244872785",
            "pic": 109951163244872785
          },
          "dt": 321549,
          "h": {
            "br": 320000,
            "fid": 0,
            "size": 12866886,
            "vd": -1.48
          },
          "m": {
            "br": 160000,
            "fid": 0,
            "size": 6433973,
            "vd": -1.04
          },
          "l": {
            "br": 96000,
            "fid": 0,
            "size": 3860807,
            "vd": -1.08
          },
          "a": None,
          "cd": "1",
          "no": 10,
          "rtUrl": None,
          "ftype": 0,
          "rtUrls": [],
          "djId": 0,
          "copyright": 2,
          "s_id": 0,
          "mark": 0,
          "originCoverType": 0,
          "rurl": None,
          "mst": 9,
          "cp": 13009,
          "mv": 5570742,
          "rtype": 0,
          "publishTime": 1190217600007
        }
      ],
      "privileges": [
        {
          "id": 29005677,
          "fee": 8,
          "payed": 0,
          "st": 0,
          "pl": 128000,
          "dl": 0,
          "sp": 7,
          "cp": 1,
          "subp": 1,
          "cs": False,
          "maxbr": 999000,
          "fl": 128000,
          "toast": False,
          "flag": 0,
          "preSell": False,
          "playMaxbr": 999000,
          "downloadMaxbr": 999000
        }
      ],
      "code": 200
    }
    push_download(data)
    ret = pop_download()
    print(json.dumps(ret, ensure_ascii=False))
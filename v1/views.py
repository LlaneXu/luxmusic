# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-29 11:17
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : views.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import
from core.response import Response, ResponseException, check_params
from core import netease
# module level variables here

# Create your models here.


class Personalized(Response):
    request_map = {
        "netease": {
            "method": "POST",
            "url": "https://music.163.com/weapi/personalized/playlist",
            "data": {
                "limit": 30,
                # offset: query.offset || 0,
                "total": True,
                "n": 1000
            },
        },
    }

    def get(self, request, json_data, *args, **kwargs):
        """
        example:
        localhost:8000/api/v1/specialized/netease/
        :param request:
        :param json_data:
        :param args:
        :param kwargs:
        :return:
        [{
          "id": 3233380300,
          "type": 0,
          "name": "歌手·当打之年1-8期现场及原曲合集",
          "copywriter": "编辑推荐：《歌手·当打之年》第1-8期竞演曲目全收录",
          "picUrl": "https://p2.music.126.net/GMy_E4iX4_IVWGHMw5bwZw==/109951164685568806.jpg",
          "canDislike": false,
          "trackNumberUpdateTime": 1585317654901,
          "playCount": 55286784,
          "trackCount": 133,
          "highQuality": false,
          "alg": "featured"
        },]
        """
        platform = kwargs["platform"]
        options = self.request_map.get(platform)
        if not options:
            raise ResponseException("unrecognized platform: %s" % platform)

        response = netease.request(options)
        response_json = response.json()
        ret = response_json["result"]
        return ret


class Playlist(Response):
    def get(self, request, json_data, *args, **kwargs):
        """

        :param request:
        :param json_data:
        :param args:
        :param kwargs:
        :return:
        {
            "id":,
            "name":
            "description": "",
            "tracks": [{
                "id":
                "name":
                "ar": [{
                    "id":
                    "name"
                }]
            }],
            "coverImgUrl":

        }
        """
        request_map = {
            "netease": {
                "method": "POST",
                "url": "https://music.163.com/weapi/v3/playlist/detail",
                "data": {
                    "id": request.GET.get("id"),
                    "n": 100000,
                    "s": 8,
                },
            },
        }
        platform = kwargs["platform"]
        options = request_map.get(platform)
        if not options:
            raise ResponseException("unrecognized platform: %s" % platform)

        required_keys = ["id"]
        check_params(request, required_keys)

        response = netease.request(options)
        response_json = response.json()
        r = response_json["playlist"]
        ret = {
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "tracks": r["tracks"],
            "coverImgUrl": r["coverImgUrl"],
            "tags": r["tags"],
        }
        return ret


class Album(Response):
    request_map = {
        "netease": {
            "method": "POST",
            "url": "https://music.163.com/weapi/v1/album/",
            "data": {},
        },
    }

    def get(self, request, json_data, *args, **kwargs):
        platform = kwargs["platform"]
        options = self.request_map.get(platform)
        if not options:
            raise ResponseException("unrecognized platform: %s" % platform)

        required_keys = ["id"]
        check_params(request, required_keys)
        options["url"] = options["url"]+request.GET["id"]

        response = netease.request(options)
        response_json = response.json()
        ret = {
            "songs": response_json["songs"],
            "album": response_json["album"]
        }
        return ret


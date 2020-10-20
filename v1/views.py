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
import logging
# 3rd import

# self import
from core.response import Response, ResponseException, check_params
from core import netease
from core.utils import map_json
from meta import models
from core.media import get_url_from_meta
from core.redis_queue import push_download
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
        ret = response["result"]
        return ret


class Playlist(Response):
    def get(self, request, json_data, *args, **kwargs):
        """

        http://localhost:8000/api/v1/playlist/netease/?id=4900028836
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
                "ar": [{   ar->artists
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
        r = response["playlist"]
        tracks = []
        key_map = (("ar", "artists"), ("al", "album"))
        for track in r["tracks"]:
            map_json(track, key_map)
            tracks.append(track)

        ret = {
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "tracks": tracks,
            "picUrl": r["coverImgUrl"],
            "tags": r["tags"],
            "playCount": r["playCount"],
            "commentCount": r["commentCount"],
            "shareCount": r["shareCount"],
            "platform": "netease",
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
        ret = {
            "songs": response["songs"],
            "album": response["album"]
        }
        return ret


class Song(Response):
    def get(self, request, json_data, *args, **kwargs):
        """
        http://localhost/api/v1/url/<platform>/?id=xx&uuid=xx&netease_id=xx&name=xx&artists=xx&album=xx
        platform: local | netease | kugou | qq
        when platform =local, need id or uuid or netease_id or name+artists (+album)
        when platform = others, just need id
        :param request:
        :param json_data:
        :param args:
        :param kwargs:
        :return:
        """
        def parse_netease(data):
            return data

        id = request.GET.get("id")
        request_map = {
            "netease": {
                "method": "POST",
                "url": "https://music.163.com/weapi/v3/song/detail",
                "data": {
                    "c": '[{"id": %s}]' % id,
                    "ids": "[%s]" % id,
                },
                "func": parse_netease,
            },
        }
        platform = kwargs["platform"]
        options = request_map.get(platform)
        if not options:
            raise ResponseException("unrecognized platform: %s" % platform)
        required_keys = ["id"]
        check_params(request, required_keys)
        response = netease.request(options)
        func = options["func"]

        return func(response)



class Url(Response):
    def get_local(self, request):
        id = request.GET.get('id')
        netease_id = request.GET.get('neteaseId')
        artists = request.GET.getlist('artists')
        name = request.GET.get('name')
        album = request.GET.get('album')

        ret = {}
        # use id to query first
        try:
            if id:
                song = models.Song.objects.get(id=id, downloaded=True)
            elif netease_id:
                song = models.Song.objects.get(netease_id=netease_id, downloaded=True)
            elif artists and len(artists) and name:
                songs = models.Song.objects.filter(downloaded=True)
                for artist in artists:
                    songs = songs.filter(artists__name__exact=artist)
                if album:
                    songs = songs.filter(album__name=album)
                if name:
                    songs = songs.filter(name=name)
                if not songs.exists():
                    return {}
                else:
                    song = songs[0]
            else:
                raise ResponseException("not enough params")

            ret = song.to_dict()
            ret["url"] = get_url_from_meta(ret)

        # can find the song record and downloaded, return local file
        except models.Song.DoesNotExist:
            print("push download (netease): id=%s" % netease_id)
            data = {
                "source": "netease",
                "id": netease_id,
            }
            push_download(data)

        return ret
    def get(self, request, json_data, *args, **kwargs):
        """
        http://localhost/api/v1/url/<platform>/?id=xx&uuid=xx&netease_id=xx&name=xx&artists=xx&album=xx
        platform: local | netease | kugou | qq
        when platform =local, need id or uuid or netease_id or name+artists (+album)
        when platform = others, just need id
        :param request:
        :param json_data:
        :param args:
        :param kwargs:
        :return:
        """
        def parse_netease(data):
            return {
                "url": data["data"][0].get("url")
            }

        id = request.GET.get("id")
        request_map = {
            "netease": {
                "method": "POST",
                "url": "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=",
                "data": {
                    "ids": "[%s]" % id,
                    "level": "standard",
                    "encodeType": "aac",
                    "csrf_token": ""
                },
                "func": parse_netease,
            },
        }
        platform = kwargs["platform"]
        if platform == "local":
            return self.get_local(request)
        else:
            options = request_map.get(platform)
            if not options:
                raise ResponseException("unrecognized platform: %s" % platform)
            required_keys = ["id"]
            check_params(request, required_keys)
            response = netease.request(options)
            func = options["func"]

            return func(response)

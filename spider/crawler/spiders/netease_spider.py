# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-27 14:23
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : netease_spider.py

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
from urllib import request
import scrapy
from scrapy.http import Request, FormRequest
from ..items import SongItem
from ..netease import encrypt_request


class Netease_Spider(scrapy.Spider):
    name = 'netease'
    # allowed_domains = ()
    _HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.122 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-real-ip": "211.161.244.70",
    }

    def __init__(self, category=None, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        self.id = id

    def _get_parse(self):
        parse_map = {
            "song": self.parse_song,
        }
        return parse_map[self.category]

    def start_requests(self):
        """
        The first request for this spider
        :return:
        """
        # return super().start_requests()
        # for url in self.start_urls:
        request_map = {
            "song": self.request_song,
        }
        # return request_map[self.category]()
        return self.request_song()

    def request_song(self):
        # get meta information first
        url = "https://music.163.com/weapi/v3/song/detail?csrf_token="
        query = {
            "c": json.dumps([{"id": self.id}]),
            "csrf_token": ""
        }
        yield FormRequest(
            url=url,
            method='POST',
            headers=self._HEADERS,
            formdata=encrypt_request(query),
            callback=self.parse_song
        )

    def parse_song(self, response):
        # decode meta information
        msg = json.loads(response.body)
        data = msg['songs']
        privileges = msg["privileges"]
        code = msg['code']
        print(json.dumps(data[0], indent=4, ensure_ascii=False))
        meta = data[0]
        item = SongItem(
            id=meta["id"],
            name=meta["name"],
            artists=meta["ar"],
            album=meta["al"],
            publishTime=meta["publishTime"]
        )

        url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
        query = {
            "ids": "[%s]" % self.id,
            "level": "standard",
            "encodeType": "aac",
            "csrf_token": ""
        }
        yield FormRequest(
            url=url,
            method='POST',
            headers=self._HEADERS,
            formdata=encrypt_request(query),
            callback=self.parse_song_file,
            meta={"item": item}
        )

    def parse_song_file(self, response):
        print("url:", response.url)
        print("meta:", response.meta)
        msg = json.loads(response.body)
        print("body:", response.body)
        code = msg['code']
        data = msg.get('data')
        if not data:
            return
        print(json.dumps(data[0], indent=4))
        item = response.meta["item"]
        url = data[0]['url']
        if not url:
            print("no download url")
            return
        item["file_urls"] = [url]
        path = "%s - %s" % (item["artists"][0]["name"], item["name"])
        print(path)
        item["files"] = ["%s - %s" % (item["artists"][0]["name"], item["name"])]
        return item



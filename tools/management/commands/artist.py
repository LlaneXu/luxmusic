# -*- coding: utf-8 -*-
"""
@Time    : 2020-10-15 18:21
@Author  : Lei Xu
@Email   : lei.xu.job.us@gmail.com
@File    : artist.py

Description:

Update:

Todo:


"""
# system import
import requests
# 3rd import
from django.core.management.base import BaseCommand, CommandError

# self import
from core import netease
# module level variables here

# Create your models here.


class Command(BaseCommand):
    help = "get all the comments of an artist's all songs"

    def add_arguments(self, parser):
        parser.add_argument('artist', nargs=1, help="the id of an artist")

    def handle(self, *args, **options):

        artist_id = options["artist"][0]
        songs = self.get_song_list(artist_id)
        for item in songs:
            print(item["name"], item["id"])
        comments = self.get_comment(songs[0]["id"])
        for item in comments:
            print(item["user"]["userId"], item["user"]["nickname"], item["content"])
            user_profile = self.get_user_info(item["user"]["userId"])
            print(user_profile["city"], user_profile["birthday"], user_profile["gender"])

    def get_song_list(self, artist_id):
        """
        https://music.163.com/weapi/artist/top/song
        post
        encrypted request
        data:
        {id: xxx}
        :return:
        """
        options = {
            "url": "https://music.163.com/weapi/artist/top/song",
            "data": {
                "id": artist_id,
                # "csrf_token": ""
            }
        }
        res = netease.request(options)
        return res.get("songs", [])

    def get_comment(self, song_id):
        """
        http://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit={limit}&offset={offset}
        :return:
        """
        url = "http://music.163.com/api/v1/resource/comments/R_SO_4_%s?limit=100&offset=%s" % (
            song_id, 1
        )
        res = requests.get(url).json()
        return res.get("comments", [])

    def get_user_info(self, user_id):
        """
        https://music.163.com/api/v1/user/detail/{user_id}
        :return:
        gender: 0-unknown, 1-male, 2-female
        birthday: ms timestamp
        city: may be empty
        """
        url = "https://music.163.com/api/v1/user/detail/%s" % (
            user_id
        )
        res = requests.get(url).json()
        return res.get("profile", {})

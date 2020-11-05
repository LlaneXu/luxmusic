# -*- coding: utf-8 -*-
"""
@Time    : 2020-10-23 21:02
@Author  : Lei Xu
@Email   : lei.xu.job.us@gmail.com
@File    : crawler_artist.py

Description:
song id list:
65766
1488563891
65538
65533
28563317
65536
551816010
65800
65528
64561
66282
35403523
64634
65919
31877628
64093
28481103
64317
1468192805
28481818
64293
65923
65761
27867449
66285
1462659723
64443
64048
64126
65312
64922
25730757
64797
31426608
65769
64833
65904
27483204
66272
64638
27483203
437802725
64625
186331
25638273
65758
64803
66265
27483202
65900

Update:

Todo:


"""
# system import
import os
import sys
import requests
import time
import random
import datetime
import multiprocessing
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
        artist, songs = get_artist_info(artist_id)
        artist_obj, created = Artist.objects.get_or_create(
            netease_id=artist["id"],
            defaults={"name": artist["name"]}
        )
        for song in songs:
            process_song(song, artist_obj)
        print("all done")


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.122 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "x-real-ip": "211.161.244.70",
    # "Cookie": "NMTID=00OmYrUWn7kjnrMiEghv8VtKW-mDz8AAAF0wg82nQ; csrftoken=MfSAeFq1h34wVW5ZZkg5O2mydtQzEPDwK5L8giRb0AxzJ1K9n6pVdfbznJIdWeJg",
    "Referer": "https://music.163.com",
}


def save_comments(comments, song_obj):
    """
    [{
        beReplied:[{
            user: {
                userId: xx,
                nickname: xx,
            }
            beRepliedCommentId: xx,
            content: xx
        }],
        user: {
            userId: xx,
            nickname: xx,
        },
        commentId: xx,
        content: xxx,
    }]
    :param comments:
    :param song_obj:
    :return:
    """
    user_saved = 0
    comment_saved = 0
    comment_processed = 0
    for comment in comments:
        try:
            comment_processed += 1
            user_id = comment["user"]["userId"]
            user_obj, created = save_user(user_id)
            if created:
                user_saved += 1
            comment_obj, created = save_comment(
                comment["commentId"],
                comment["content"],
                user_obj,
                song_obj,
            )
            if created:
                comment_saved += 1

            re_comments = comment["beReplied"]
            if re_comments and len(re_comments) >0:
                for re_comment in re_comments:
                    re_user_obj, created = save_user(re_comment["user"]["userId"])
                    if created:
                        user_saved += 1
                    re_comment_obj, created = save_comment(
                        re_comment["beRepliedCommentId"],
                        re_comment["content"],
                        re_user_obj,
                        song_obj
                    )
                    comment_obj.replied.add(re_comment_obj)
                    if created:
                        comment_saved += 1
        except Exception:
            print(comment)

    return user_saved, comment_saved, comment_processed


def save_user(user_id):
    created = False
    try:
        user_obj = User.objects.get(netease_id=user_id)
    except User.DoesNotExist:
        created = True
        user = get_user_info(user_id)
        ts = user.get("birthday", 0) / 1000
        birthday = datetime.datetime.fromtimestamp(ts) if ts > 0 else None
        user_obj = User.objects.create(
            netease_id=user["userId"],
            name=user["nickname"],
            gender=user["gender"],
            city=user.get("city", None),
            birthday=birthday,
        )
    return user_obj, created


def save_comment(comment_id, content, user_obj, song_obj):
    created = False
    try:
        comment_obj = Comment.objects.get(netease_id=comment_id)
    except Comment.DoesNotExist:
        created = True
        comment_obj = Comment.objects.create(
            netease_id=comment_id,
            user=user_obj,
            song=song_obj,
            content=content
        )
    return comment_obj, created




def get_song_list(artist_id):
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


def get_comment(song_id, page=1, cursor=-1):
    """
    http://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit={limit}&offset={offset}
    :return:
    {
        code: 200,
        data: {
            comments: [{
                beReplied:[{
                    user: {
                        userId: xx,
                        nickname: xx,
                    }
                    beRepliedCommentId: xx,
                    content: xx
                }],
                user: {
                    userId: xx,
                    nickname: xx,
                },
                commentId: xx,
                content: xxx,
            }],
            totalCount: xxx,
        }
    }
    """
    options = {
        "url": "https://music.163.com/weapi/comment/resource/comments/get?csrf_token=",
        "data": {
            "rid": "R_SO_4_%s" % song_id,
            "threadId": "R_SO_4_%s" % song_id,
            # "offset": (page-1)*100,
            "pageNo": page,
            "pageSize": 100,
            "orderType": 2,
            "cursor": cursor,
        }
    }
    res = netease.request(options)
    data = res["data"]
    return data.get("comments", []), data["totalCount"], data["cursor"]

def get_user_info(user_id):
    """
    https://music.163.com/api/v1/user/detail/{user_id}
    :return:
    {
        profile: {
            userId: xx,
            nickname: xx,
            gender: 0-unknown, 1-male, 2-female,
            birthday: ms timestamp, maybe a negative number
            city: may be empty
        }
    }
    """
    url = "https://music.163.com/api/v1/user/detail/%s" % (
        user_id
    )
    res = requests.get(url, headers=headers).json()
    return res.get("profile", {})


def process_song(song_id, thread):
    pid = os.getpid()
    cmd = "python3 manage.py song %s %s" % (song_id, thread)
    print("processing(%s-%s): %s" % (thread, pid, cmd))
    os.system(cmd)


if __name__ == "__main__":
    print("start crawling...")
    songs =[
        65766,
        1488563891,
        65538,
        65533,
        28563317,
        65536,
        551816010,
        65800,
        65528,
        64561,
        66282,
        35403523,
        64634,
        65919,
        31877628,
        64093,
        28481103,
        64317,
        1468192805,
        28481818,
        64293,
        65923,
        65761,
        27867449,
        66285,
        1462659723,
        64443,
        64048,
        64126,
        65312,
        64922,
        25730757,
        64797,
        31426608,
        65769,
        64833,
        65904,
        27483204,
        66272,
        64638,
        27483203,
        437802725,
        64625,
        186331,
        25638273,
        65758,
        64803,
        66265,
        27483202,
        65900,
    ]
    pool = multiprocessing.Pool(20)
    thread = 0
    for song in songs:
        pool.apply_async(process_song,args=(song, thread))
        thread += 1
    pool.close()
    pool.join()

    print("all done")

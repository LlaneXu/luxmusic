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
import os
import datetime
# 3rd import
from django.core.management.base import BaseCommand, CommandError

# self import
from core import netease
from meta.models import Artist, Album, Song, Comment, User
# module level variables here

# Create your models here.


class Command(BaseCommand):
    help = "get all the comments of an artist's all songs"

    def add_arguments(self, parser):
        parser.add_argument('artist', nargs=1, help="the id of an artist")

    def handle(self, *args, **options):

        artist_id = options["artist"][0]
        artist, songs = netease.get_artist_info(artist_id)
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


def process_song(song, artist_obj):
    pid = os.getpid()
    print("processing(%s): " % pid, song["name"], song["id"], artist_obj.name)
    album = song["al"]
    album_obj, created = Album.objects.get_or_create(
        netease_id=album["id"],
        defaults={
            "name": album["name"],
            "artist": artist_obj,
            "pic": album["picUrl"]
        }
    )
    song_obj, created = Song.objects.get_or_create(
        netease_id=song["id"],
        defaults={
            "name": song["name"],
            "album": album_obj,
        }
    )
    artists = song["ar"]
    for artist in artists:
        artist_obj, created = Artist.objects.get_or_create(
            netease_id=artist["id"],
            defaults={"name": artist["name"]}
        )
        song_obj.artists.add(artist_obj)

    page = 1
    saved_users = 0
    saved_comments = 0
    processed_comments = 0
    cursor = -1
    while True:
        comments, total, new_cursor = netease.get_comment(song["id"], page, cursor)
        cursor = new_cursor
        last_page = int(total / 100) + 1
        new_users, new_comments, new_processed_comments = save_comments(comments, song_obj)
        saved_users += new_users
        saved_comments += new_comments
        processed_comments += new_processed_comments
        print("(%s)saved users: %s, comments: %s/%s/%s" % (pid, new_users, new_comments, processed_comments, total))
        page += 1
        if page > last_page:
            print("(%s)total=%s, last_page=%s, page=%s" % (pid, total, last_page, page))
            break


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
        user = netease.get_user_info(user_id)
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

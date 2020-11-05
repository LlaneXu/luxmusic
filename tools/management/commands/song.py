# -*- coding: utf-8 -*-
"""
@Time    : 2020-10-23 21:48
@Author  : Lei Xu
@Email   : lei.xu.job.us@gmail.com
@File    : song.py

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
from meta.models import Song, Comment, User
from core import netease
from tools.models import Crawler
# module level variables here

# Create your models here.


class Command(BaseCommand):
    help = "get all the comments of a song"

    def add_arguments(self, parser):
        parser.add_argument('song', nargs=1, help="the id of the song")
        parser.add_argument('thread', nargs=1, help="thread index")

    def handle(self, *args, **options):
        song_id = options["song"][0]
        thread = options["thread"][0]
        pid = os.getpid()
        song_obj = Song.objects.get(netease_id=song_id)
        print("(%s-%s): start crawling %s-%s" % (thread, pid, song_id, song_obj.name))
        crawler, created = Crawler.objects.get_or_create(netease_id=song_id, defaults={"page": 1,"cursor": -1})

        page = crawler.page
        cursor = crawler.cursor
        if not created:
            print("Found crawler record! start from page=%s, cursor=%s" % (page, cursor))
        saved_users = 0
        saved_comments = 0
        processed_comments = (page-1)*100
        while True:
            crawler.page = page
            crawler.cursor = cursor
            crawler.save()
            comments, total, new_cursor = netease.get_comment(song_id, page, cursor)
            cursor = new_cursor
            last_page = int(total / 100) + 1
            new_users, new_comments, new_processed_comments = save_comments(comments, song_obj)
            saved_users += new_users
            saved_comments += new_comments
            processed_comments += new_processed_comments
            print("(%s-%s): saved users: %s, comments: %s/%s/%s (%.2f%%) (%s-%s)" % (
                thread,
                pid,
                new_users,
                new_comments,
                processed_comments,
                total,
                processed_comments/total * 100,
                song_id,
                song_obj.name,
            ))
            page += 1
            if page > last_page:
                print("(%s-%s): total=%s, last_page=%s, page=%s" % (thread, pid, total, last_page, page))
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
                    if re_comment_obj not in comment_obj.replied.all():
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


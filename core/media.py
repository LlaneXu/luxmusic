# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-05 17:26
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : media.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import

# module level variables here

# Create your models here.
from django.conf import settings


def get_artists_from_meta(meta):
    artists = [artist["name"] for artist in meta.get("artists")]
    artists.sort()
    return "&".join(artists)

def get_export_relative_path_from_meta(meta):
    filename = "%s - %s.%s" % (get_artists_from_meta(meta), meta["name"], meta["ext"])
    return "%s/%s/%s" % (get_artists_from_meta(meta), meta["album"]["name"],filename)

def get_filename_from_meta(meta):
    # return "%s - %s.%s" % (get_artists_from_meta(meta), meta["name"], meta["ext"])
    return "%s.%s" % (meta["uuid"], meta["ext"])

def get_relative_path_from_meta(meta):
    # return "%s/%s/%s" % (get_artists_from_meta(meta), meta["album"]["name"],get_filename_from_meta(meta))
    return get_filename_from_meta(meta)

def get_url_from_meta(meta):
    return "%s/%s" % (settings.MUSIC_URL, get_relative_path_from_meta(meta))

def get_path_from_meta(meta):
    """

    :param meta:
    {
        "id": "",
        "name": "",
        "artists": [{
            "name": "",
            "id": "",
        }],
        "album": {
            "id": "",
            "name": "",
        }
    }
    :param dist:
    whether get distribution folder into the path
    :return:
    """
    return "%s/%s" % (settings.MUSIC_FOLDER, get_relative_path_from_meta(meta))


def test():
    meta = {
        "name": "沧海一声笑",
        "artists": [{
            "name": "黄霑",
        }, {
            "name": "罗大佑",
        }, {
            "name": "徐克",
        }],
        "ext": "mp3"
    }
    print(get_path_from_meta(meta))

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

def get_artists_from_meta(meta):
    artists = [artist["name"] for artist in meta.get("artists")]
    artists.sort()
    return "&".join(artists)

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
    :return:
    """
    artists = get_artists_from_meta(meta)
    filename = "%s - %s.%s" % (artists, meta["name"], meta["ext"])
    return "%s/%s" % (artists, filename)


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

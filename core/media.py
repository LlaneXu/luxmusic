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
    artists = "&".join([artist["name"] for artist in meta.get("artists")])
    filename = "%s - %s.%s" % (artists, meta["name"], meta["ext"])
    return "%s/%s" % (artists, filename)
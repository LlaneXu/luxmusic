# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-25 19:24
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : import.py

Description:

Update:

Todo:


"""
# system import
import os
import shutil
# 3rd import
from django.core.management.base import BaseCommand, CommandError
from tinytag import TinyTag
# self import
from meta.models import Artist, Album, Song
from core.media import get_path_from_meta, get_export_relative_path_from_meta
from core.utils import copy

# module level variables here

# Create your models here.
class Command(BaseCommand):
    help = "export system music into a folder"

    def add_arguments(self, parser):
        parser.add_argument('path', nargs=1, help="folder used to store exported music")

    def handle(self, *args, **options):
        folder = options["path"][0]
        exported=[]
        exported_num = 0
        songs = Song.objects.filter(downloaded=True)
        abs_folder = os.path.abspath(folder)
        for song in songs:
            meta = song.to_dict()
            src_path = get_path_from_meta(meta)
            if os.path.exists(src_path):
                dest_path = os.path.join(abs_folder,get_export_relative_path_from_meta(meta))
                copy(src_path, dest_path)
                exported.append(dest_path)
                exported_num += 1
        print("exported(%s):" % exported_num)
        print("\n".join(exported))


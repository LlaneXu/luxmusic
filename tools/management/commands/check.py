# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-08 12:37
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : check.py

Description:

Update:

Todo:


"""
# system import
import os
import shutil
import uuid
# 3rd import
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
# self import
from meta.models import Song
from core.media import get_path_from_meta, get_filename_from_meta
# module level variables here

# Create your models here.

class Command(BaseCommand):
    help = "check all music downloaded status"

    def handle(self, *args, **options):
        songs = Song.objects.all()
        exists_not_downloaded = 0
        exists_not_downloaded_list = []
        not_exists_downloaded = 0
        not_exists_downloaded_list = []
        archived_num = 0
        archived = []
        for song in songs:
            meta = song.to_dict()
            path = get_path_from_meta(meta)
            if os.path.exists(path) and song.downloaded == False:
                exists_not_downloaded += 1
                exists_not_downloaded_list.append(get_filename_from_meta(meta))
                song.downloaded = True
            elif not os.path.exists(path) and song.downloaded == True:
                not_exists_downloaded += 1
                not_exists_downloaded_list.append(get_filename_from_meta(meta))
                song.downloaded = False
            song.save()
        root = settings.MUSIC_FOLDER
        archived_folder = "archived"
        if not os.path.exists(archived_folder):
            os.mkdir(archived_folder)
        for file in os.listdir(root):
            src_full = os.path.join(root, file)
            if os.path.isfile(src_full):
                name, ext = os.path.splitext(file)
                if ext in ('.m4a', '.mp3', "ape", "flac"):
                    exists = False
                    try:
                        uuid_name = uuid.UUID(name)
                        a = Song.objects.filter(uuid=uuid_name)
                        if a.exists():
                            exists = True
                    except ValueError:
                        pass
                    finally:
                        if not exists:
                            dst_full = os.path.join(root,archived_folder,file)
                            shutil.move(src_full, dst_full)
                            archived.append(file)
                            archived_num += 1

        print("File exists but status = not downloaded (%s):" % exists_not_downloaded)
        print("\n".join(exists_not_downloaded_list))
        print("File doesn't exist but status = download (%s):" % not_exists_downloaded)
        print("\n".join(not_exists_downloaded_list))
        print("Archived unknown file(%s):" % archived_num)
        print("\n".join(archived))

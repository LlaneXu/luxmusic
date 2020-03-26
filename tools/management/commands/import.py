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
from core.media import get_path_from_meta

# module level variables here

# Create your models here.
class Command(BaseCommand):
    help = "import music into system"

    def add_arguments(self, parser):
        parser.add_argument('path', nargs=1, help="music folder need to be imported")

    def handle(self, *args, **options):
        folder = options["path"][0]
        passed=[]
        passed_num = 0
        downloaded = []
        downloaded_num = 0
        moved=[]
        moved_num = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                ext = os.path.splitext(file)[-1]
                if ext in ('.m4a', '.mp3', "ape", "flac"):
                    filename = os.path.abspath(os.path.join(root, file))
                    tag = TinyTag.get(filename)
                    artists = tag.artist.split('&') if tag.artist else []
                    album = tag.album
                    title = tag.title
                    if len(artists)==0 or not album or not title:
                        passed_num += 1
                        passed.append(filename)
                    else:
                        artists_obj = []
                        for artist in artists:
                            obj, created = Artist.objects.get_or_create(name=artist)
                            artists_obj.append(obj)
                        album_obj, created = Album.objects.get_or_create(name=album)

                        songs = Song.objects.filter(name=title)
                        for obj in artists_obj:
                            songs = songs.filter(artists=obj)
                        songs = songs.filter(album=album_obj)
                        if songs:
                            song = songs[0]
                        else:
                            song = Song.objects.create(
                                name=title,
                                album=album_obj
                            )
                            for obj in artists_obj:
                                song.artists.add(obj)
                            song.save()
                        if song.downloaded:
                            downloaded_num += 1
                            downloaded.append(filename)
                        else:
                            meta = song.to_dict()
                            new_path = get_path_from_meta(meta)
                            shutil.copy(filename, new_path)
                            song.downloaded = True
                            song.save()
                            moved_num += 1
                            moved.append('%s -> %s' % (filename, new_path))
        print("passed (%s): " % passed_num)
        print("\n".join(passed))
        print("\nalready have (%s): " % downloaded_num)
        print("\n".join(downloaded))
        print("\nmoved (%s): " % moved_num)
        print("\n".join(moved))

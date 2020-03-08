# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import logging
import subprocess
import datetime
from scrapy.pipelines.files import FilesPipeline
from meta.models import Artist, Album, Song
from django.utils import timezone
from core.media import get_relative_path_from_meta, get_artists_from_meta


class SongPipeline(FilesPipeline):
    def process_item(self, item, spider):
        self.item = item
        artists = item["artists"]
        album = item["album"]

        artists_obj = []
        for artist in artists:
            obj, created = Artist.objects.update_or_create(
                netease_id=artist["id"],
                defaults={"name": artist["name"]}
            )
            artists_obj.append(obj)
        ts = item["publishTime"]
        if ts > 10000000000:
            ts /= 1000
        tz = timezone.get_current_timezone()
        publish_time = datetime.datetime.fromtimestamp(ts, tz)
        album_obj, created = Album.objects.update_or_create(
            netease_id=album["id"],
            defaults={
                "name": album["name"],
                "pic": album["picUrl"],
                "publish_time": publish_time
            }
        )
        song_obj, created = Song.objects.update_or_create(
            netease_id=item["id"],
            defaults={
                "name": item["name"],
                "album": album_obj,
                "source": "netease",
            }
        )
        for obj in artists_obj:
            song_obj.artists.add(obj)
        song_obj.save()
        if song_obj.downloaded:
            logging.warning("%s has been downloaded" % song_obj.name)
            return
        if len(item.get("file_urls",[])) == 0:
            logging.warning("%s no url")
            return
        self.song_obj = song_obj
        return super().process_item(item, spider)

    def file_path(self, request, response=None, info=None):
        return get_relative_path_from_meta(self.item)
        # artists = "&".join([artist["name"] for artist in self.item["artists"]])
        # filename = "%s - %s.m4a" % (artists, self.item["name"])
        # return "%s/%s" % (artists, filename)

    def item_completed(self, results, item, info):
        """
        add id3 tag into file
        :param results:
        :param item:
        :param info:
        :return:
        """
        cmd = ["ffmpeg", "-i"]
        #
        path = results[0][1]["path"]
        settings = self.spiderinfo.spider.settings
        folder = settings.get("FILES_STORE")
        path = os.path.join(folder, path)
        abspath = os.path.abspath(path)
        name, ext = os.path.splitext(abspath)
        newpath = "%s_id3%s" % (name, ext)
        cmd.append(abspath)
        cmd.append("-metadata")
        cmd.append("artist=%s" % get_artists_from_meta(item))
        cmd.append("-metadata")
        cmd.append("album=%s" % item["album"]["name"])
        cmd.append("-metadata")
        cmd.append("title=%s" % item["name"])

        cmd.append("-acodec")
        cmd.append("copy")
        cmd.append("-y")

        cmd.append(newpath)
        subprocess.call(cmd)
        os.rename(newpath, abspath)
        logging.info("downloaded: %s" % abspath)
        self.song_obj.downloaded = True
        self.song_obj.save()
        return item

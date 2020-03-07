# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-06 16:28
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : run.py

Description:

Update:

Todo:


"""
# system import
import os
# 3rd import
from django.core.management.base import BaseCommand, CommandError
from scrapy import cmdline
# self import
from core.redis_queue import pop_download
# module level variables here

# Create your models here.

class Command(BaseCommand):
    help = "download daemon, get download information from redis"

    def handle(self, *args, **options):
        """
        download information example
        {
            "source": "netease", # netease/qq/kugou,
            "id": 123456,
        }
        :param args:
        :param options:
        :return:
        """
        old_path = os.getcwd()
        new_path = os.path.join(old_path, "spider")
        os.chdir(new_path)

        while True:
            item = pop_download()
            source = item.get("source")
            id = item.get("id")
            if source == "netease":
                cmd = "scrapy crawl netease -a category=song -a id=%s" % id
                os.system(cmd)

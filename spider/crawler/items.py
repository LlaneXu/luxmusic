# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SongItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    artists = scrapy.Field()    # 艺术家，list
    album = scrapy.Field()      # 专辑
    title = scrapy.Field()      # 歌曲名
    publishTime = scrapy.Field()
    file_urls = scrapy.Field()        # 歌曲下载地址
    files = scrapy.Field()       # 本地地址
    ext = scrapy.Field()

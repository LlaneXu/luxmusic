from django.db import models
from core.models import Model
from core import utils

# Create your models here.

class Artist(Model):
    netease_id = models.IntegerField(null=True, blank=True)
    # name = models.CharField(max_length=32)
    pic = models.CharField(max_length=255, null=True, blank=True)

    # keys, json_keys, object_keys, and many2many_keys are optional
    # if they are defined, only the values of keys in these list will be exposed to api,
    # default:  all non-object keys in this object, including pk or id
    # keys = ("id", "netease_id", "name", "pic",)

    # values of json_keys will be transformed by json.loads
    # json_keys = ()

    # value of foreign_keys will be translated by the to_dict of its object
    # default: all foreign keys
    # foreign_keys = ()

    # translated as a list
    # many2many_keys = ()

    #
    # def __str__(self):
    #     return self.name

    # def to_dict(self):
    #     ret = utils.queryset_to_js(self)
    #     return ret


class Album(Model):
    netease_id = models.IntegerField(null=True, blank=True)
    # name = models.CharField(max_length=32)
    pic = models.CharField(max_length=255, null=True, blank=True)
    publish_time = models.DateTimeField(default=None, null=True, blank=True)


    # def __str__(self):
    #     return self.name
    #
    # def to_dict(self):
    #     ret = utils.queryset_to_js(self)
    #     return ret


class Song(Model):
    netease_id = models.IntegerField(null=True, blank=True)
    # name = models.CharField(max_length=32)
    artists = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    downloaded = models.BooleanField(default=False)
    ext = models.CharField(max_length=16, choices=(
        ('m4a', 'm4a'),
        ('mp3', 'mp3'),
        ('ape', 'ape'),
        ('flac', 'flac'),
    ), default='m4a')
    source = models.CharField(max_length=16, choices=(
        ('netease', '网易云音乐'),
        ('qq', 'qq音乐'),
        ('kugou', '酷狗音乐'),
    ), null=True, blank=True)


    # def __str__(self):
    #     return self.name
    #
    # def to_dict(self):
    #     ret = utils.queryset_to_js(self)
    #     return ret

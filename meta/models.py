from django.db import models
from core import utils

# Create your models here.

class Artist(models.Model):
    netease_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=32)
    pic = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        ret = utils.attr_to_dict(self)
        return ret


class Album(models.Model):
    netease_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=32)
    pic = models.CharField(max_length=255, null=True, blank=True)
    publish_time = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        ret = utils.attr_to_dict(self)
        return ret


class Song(models.Model):
    netease_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=32)
    artists = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def to_dict(self):
        ret = utils.attr_to_dict(self)
        return ret

import uuid
from django.db import models
from core.models import ModelWithName, UUIDFieldNoDash
from core import utils
from django.utils.html import format_html

# Create your models here.

class Artist(ModelWithName):
    netease_id = models.BigIntegerField(null=True, blank=True)
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


class Album(ModelWithName):
    netease_id = models.BigIntegerField(null=True, blank=True)
    # name = models.CharField(max_length=32)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    pic = models.CharField(max_length=255, null=True, blank=True)
    publish_time = models.DateTimeField(default=None, null=True, blank=True)


    # def __str__(self):
    #     return self.name
    #
    # def to_dict(self):
    #     ret = utils.queryset_to_js(self)
    #     return ret


class Song(ModelWithName):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    netease_id = models.BigIntegerField(null=True, blank=True)
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


    def __str__(self):
        artists = "&".join([artist.name for artist in self.artists.all()])
        return "%s - %s(%s)" % (artists, self.name, self.album)
    #
    # def to_dict(self):
    #     ret = utils.queryset_to_js(self)
    #     return ret



class User(ModelWithName):
    netease_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('0', 'Unknown'), ('1', "male"), ("2", "female")))
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    province = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)


class Comment(models.Model):
    netease_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    replied = models.ManyToManyField("self", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

    def replies(self):
        return "|".join([str(item) for item in self.replied.all()])

    def replies_link(self):
        html_strings=[]
        for item in self.replied.all():
            html_strings.append(
            '<div><a href="/admin/meta/comment/%s/change/">%s</a><div>' % (item.id, str(item))
            )
        return format_html(
            '<span>'+''.join(html_strings)+'</span>'
        )
        # return "replies"

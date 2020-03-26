from django.contrib import admin
from . import models
# Register your models here.
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "netease_id", "name")
    readonly_fields = ("id",)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "netease_id", "name", "pic", "publish_time")
    readonly_fields = ("id",)


class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "netease_id", "name", "artist", "album", "source", "downloaded", "ext",)
    readonly_fields = ("id", "uuid",)

    def artist(self, obj):
        return '&'.join([str(a) for a in obj.artists.all()])

admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Song, SongAdmin)

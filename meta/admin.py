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


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "birthday")
    readonly_fields = ("id",)


class CommentAdmin(admin.ModelAdmin):
    fields = ("id", "netease_id", "user", "song", "content", "replies_readonly")
    list_display = ("id", "user", "song", "content", "replies")
    readonly_fields = ("id", "replies_readonly",)

    def replies_readonly(self, instance):
        return instance.replies_link()

admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Song, SongAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Comment, CommentAdmin)

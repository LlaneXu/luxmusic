from django.contrib import admin
from . import models
# Register your models here.
class CrawlerAdmin(admin.ModelAdmin):
    list_display = ("id", "netease_id", "page", "cursor")
    readonly_fields = ("id",)

class AnalyzeCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "tag", "counts")
    readonly_fields = ("id",)

class ProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "processed", "target")
    readonly_fields = ("id",)


admin.site.register(models.Crawler, CrawlerAdmin)
admin.site.register(models.AnalyzeComment, AnalyzeCommentAdmin)
admin.site.register(models.Progress, )

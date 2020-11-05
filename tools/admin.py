from django.contrib import admin
from . import models
# Register your models here.
class CrawlerAdmin(admin.ModelAdmin):
    list_display = ("id", "netease_id", "page", "cursor")
    readonly_fields = ("id",)


admin.site.register(models.Crawler, CrawlerAdmin)

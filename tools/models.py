from django.db import models

# Create your models here.

class Crawler(models.Model):
    netease_id = models.BigIntegerField(null=True, blank=True)
    page = models.IntegerField(default=1, null=True, blank=True)
    cursor = models.BigIntegerField(default=-1, null=True, blank=True)

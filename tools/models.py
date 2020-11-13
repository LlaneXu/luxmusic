from django.db import models

# Create your models here.

class Crawler(models.Model):
    netease_id = models.BigIntegerField(null=True, blank=True)
    page = models.IntegerField(default=1, null=True, blank=True)
    cursor = models.BigIntegerField(default=-1, null=True, blank=True)

class AnalyzeComment(models.Model):
    word = models.CharField(max_length=16, db_index=True)
    word_en = models.CharField(max_length=16, null=True, blank=True)
    tag = models.CharField(max_length=16)
    counts = models.BigIntegerField(default=0)

class Progress(models.Model):
    name = models.CharField(max_length=16)
    processed = models.IntegerField(default=0)
    target = models.IntegerField(default=0)

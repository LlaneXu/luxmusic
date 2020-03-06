# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-06 10:07
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : models.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import

# module level variables here

# Create your models here.
from django.db import models
from .utils import queryset_to_js

class Model(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def to_dict(self):
        return queryset_to_js(self)

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
from django.db.models import UUIDField
# self import

# module level variables here

# Create your models here.
from django.db import models
from .utils import queryset_to_js

class ModelWithName(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def to_dict(self):
        return queryset_to_js(self)


class UUIDFieldNoDash(UUIDField):
    def __str__(self):
        print("str")
        return super().__str__()

    def to_python(self, value):
        print('to python')
        ret = super().to_python(value)
        return ret

    def get_prep_value(self, value):
        print('prep_value')
        return super().get_prep_value(value)

    def value_from_object(self, obj):
        print('value')
        return super().value_from_object(obj)

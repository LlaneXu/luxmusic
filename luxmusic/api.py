# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-01 16:51
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : api.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import

# module level variables here

# Create your models here.


from django.urls import path, include

urlpatterns = [
    path('meta/', include("meta.url")),
]

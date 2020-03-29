# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-29 11:13
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : urls.py

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
from . import views

urlpatterns = [
    path('personalized/<path:platform>/', views.Personalized()),
    path('playlist/<path:platform>/', views.Playlist()),
    path('album/<path:platform>/', views.Album()),
]
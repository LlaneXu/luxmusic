# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-01 16:52
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : url.py

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
    path('song/', views.SongView()),
]


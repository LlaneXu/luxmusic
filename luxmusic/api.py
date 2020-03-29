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


from django.urls import path, include, re_path
from .views import proxy_view

urlpatterns = [
    path('meta/', include("meta.urls")),
    path('v1/', include("v1.urls")),

    path('<path:path>', proxy_view),
]

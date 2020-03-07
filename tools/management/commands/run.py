# -*- coding: utf-8 -*-
"""
@Time    : 2020-03-06 16:28
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : run.py

Description:

Update:

Todo:


"""
# system import
import importlib
# 3rd import
from django.core.management.base import BaseCommand, CommandError
# self import

# module level variables here

# Create your models here.

class Command(BaseCommand):
    help = "run any function in any file"

    def add_arguments(self, parser):
        parser.add_argument('function', nargs=1, help="{package}.{file}.{function}")
        parser.add_argument('--params', action="append", help="args of function")

    def handle(self, *args, **options):
        function_str = options["function"][0].split(".")
        params = options.get("params")
        package = importlib.import_module(".".join(function_str[:-1]))
        func = getattr(package, function_str[-1])
        if params:
            func(*params)
        else:
            func()

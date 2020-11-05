# -*- coding: utf-8 -*-
"""
@Time    : 2020-10-23 15:08
@Author  : Lei Xu
@Email   : lei.xu.job.us@gmail.com
@File    : analyse.py

Description:

Update:

Todo:


"""
# system import
import collections

# 3rd import
from django.core.management.base import BaseCommand, CommandError
import pkuseg

# self import
from meta.models import Comment, User
# module level variables here

# Create your models here.


class Command(BaseCommand):
    help = "analyze comments or user"

    def add_arguments(self, parser):
        parser.add_argument('target', choices=('user','comment'), help="the entity to analyze")

    def handle(self, *args, **options):
        if options["target"] == "comment":
            self.analyze_comment()
        else:
            pass
        print("all done")

    def analyze_comment(self):
        comments = Comment.objects.all()[:10000]
        seg = pkuseg.pkuseg(model_name="web", postag=True)
        # seg = pkuseg.pkuseg(model_name="web", postag=False)
        counter = collections.Counter()
        for comment in comments:
            words = seg.cut(comment.content)
            filtered = []
            for item in words:
                if item[1] not in ('w',):
                    filtered.append(item[0])
            counter.update(filtered)
        print(counter.most_common(50))

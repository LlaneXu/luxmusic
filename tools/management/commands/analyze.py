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
from tools.models import AnalyzeComment, Progress
# module level variables here

# Create your models here.


class Command(BaseCommand):
    help = "analyze comments or user"

    def add_arguments(self, parser):
        parser.add_argument('target', choices=('user','comment', 'translate'), help="the entity to analyze")

    def handle(self, *args, **options):
        if options["target"] == "comment":
            self.analyze_comment()
        elif options["target"] == "translate":
            self.translate()
        else:
            pass
        print("all done")

    def analyze_comment(self):
        total = Comment.objects.count()
        step = 50000
        seg = pkuseg.pkuseg(model_name="web", postag=True)
        counter = collections.Counter()

        progress, _ = Progress.objects.get_or_create(
            name="analyze_comment",
            defaults={
                "target":total
            }
        )
        processed = progress.processed
        while processed <= total:
            comments = Comment.objects.all()[processed:processed+step]
            for comment in comments:
                words = seg.cut(comment.content)
                filtered = []
                for item in words:
                    filtered.append((item[1],item[0]))
                counter.update(filtered)
            print("%s/%s(%.2f%%)" % (processed, total, processed/total))
            for key,value in counter.items():
                tag,word = key
                try:
                    record, _ = AnalyzeComment.objects.get_or_create(
                        word=word,
                        tag=tag,
                    )
                    record.counts += value
                    record.save()
                except:
                    print("invalid: ", word)
            counter.clear()

            processed += step
            progress.processed = processed
            progress.save()

    def translate(self):
        import translators as ts
        data = AnalyzeComment.objects.filter(tag="n").order_by("-counts")[:200]
        p = 0
        for item in data:
            p += 1
            if not p % 100:
                print(p)
            ch = item.word
            if item.word_en:
                continue
            en = ts.google(ch)
            try:
                item.word_en = en
                item.save()
            except:
                print(en)


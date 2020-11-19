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
import pyecharts.options as opts
from pyecharts.charts import WordCloud, Bar, Pie
# self import
from meta.models import Comment, User
from tools.models import AnalyzeComment, Progress
# module level variables here

# Create your models here.


class Command(BaseCommand):
    help = "analyze comments or user"

    def add_arguments(self, parser):
        parser.add_argument('target', choices=('user','comment'), help="the entity to analyze")

    def handle(self, *args, **options):
        if options["target"] == "comment":
            self.show_comment()
        else:
            self.show_user()

    def show_comment(self):
        alls = AnalyzeComment.objects.all().order_by('-counts')
        lans = ("zh", "en")
        tags = ("", "v", "n", "a")
        for lan in lans:
            for tag in tags:
                file = "analysis/%s_%s.html" % (lan, tag)
                if not tag:
                    objs = alls[:200]
                else:
                    objs = alls.filter(tag=tag)[:200]
                if lan == "zh":
                    data = [(item.word, item.counts) for item in objs]
                else:
                    data = [(item.word_en, item.counts) for item in objs]
        # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
        # 也可以传入路径参数，如 bar.render("mycharts.html
                (
                    WordCloud()
                        .add(series_name="word analysis", data_pair=data, word_size_range=[10,200])
                        .set_global_opts(
                        title_opts=opts.TitleOpts(
                            title="word frequency", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                        ),
                        tooltip_opts=opts.TooltipOpts(is_show=True),
                    )
                    .render(file)
                )

    def show_user(self):
        # self.gender()
        self.age()

    def gender(self):
        all = User.objects.count()
        males = User.objects.filter(gender=1).count()
        females = User.objects.filter(gender=2).count()
        unknown = all - males - females
        c = (
            Pie()
                .add("", [("male",males), ("female",females), ("unknown",unknown)])
                .set_colors(["blue", "red", "orange"])
                .set_global_opts(title_opts=opts.TitleOpts(title="Gender"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))
                .render("analysis/gender.html")
        )

    def age(self):
        pass

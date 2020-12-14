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
from django.db.models import Count
import pyecharts.options as opts
from pyecharts.charts import WordCloud, Bar, Pie, Map
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
        # self.age()
        self.city()

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
        all = User.objects.filter(age__gt=1).values("age").annotate(Count("id"))

        xdata = [x for x in range(0,70)]
        ydata = [0]*70
        for one in all:
            ydata[one["age"]] = one["id__count"]
        c = (
            Bar()
            .add_xaxis(xdata[10:41])
            .add_yaxis("", ydata[10:41],color="blue",label_opts=None)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Age Distribution"),
                xaxis_opts=opts.AxisOpts(name="Age"),
                yaxis_opts=opts.AxisOpts(name="Count"),
            )
                .render("analysis/age_distribution.html")
        )

    def city(self):
        city_map = {
            '11': '北京',
            '12': '天津',
            '31': '上海',
            '50': '重庆',
            '5e': '重庆',
            '81': '香港',
            '82': '澳门',
            '13': '河北',
            '14': '山西',
            '15': '内蒙古',
            '21': '辽宁',
            '22': '吉林',
            '23': '黑龙江',
            '32': '江苏',
            '33': '浙江',
            '34': '安徽',
            '35': '福建',
            '36': '江西',
            '37': '山东',
            '41': '河南',
            '42': '湖北',
            '43': '湖南',
            '44': '广东',
            '45': '广西',
            '46': '海南',
            '51': '四川',
            '52': '贵州',
            '53': '云南',
            '54': '西藏',
            '61': '陕西',
            '62': '甘肃',
            '63': '青海',
            '64': '宁夏',
            '65': '新疆',
            '71': '台湾',
            # '10': '其他',
        }
        all = User.objects.values("province").annotate(Count("id"))
        data=[]
        min_data = float("inf")
        max_data = float("-inf")
        for one in all:
            key = city_map.get(one["province"])
            value = one["id__count"]
            if key:
                data.append([key, value])
                if value>max_data:
                    max_data = value
                if value < min_data:
                    min_data = value
        c = (
            Map()
            .add(
                "",
                data,
                "china",
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Province Distribution"),
                visualmap_opts=opts.VisualMapOpts(
                    min_=min_data,
                    max_=max_data,
                    range_color=["aliceblue", "deepskyblue", "midnightblue"],
                ),
            )
                .render("analysis/province_distribution.html")
        )

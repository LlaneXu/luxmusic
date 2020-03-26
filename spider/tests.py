from django.test import TestCase
import os

# Create your tests here.
from scrapy import cmdline

class SpiderTest(TestCase):
    def setUp(self):
        self.old_path = os.getcwd()
        self.new_path = os.path.join(self.old_path, "spider")
        os.chdir(self.new_path)

    def tearDown(self):
        os.chdir(self.old_path)

    def test_song(self):
        # cmdline.execute("scrapy list".split())
        cmdline.execute("scrapy crawl netease -a category=song -a id=5237745".split())
        self.assertTrue(True)

# cmdline.execute("scrapy crawl netease -a category=song -a id=29005677".split())

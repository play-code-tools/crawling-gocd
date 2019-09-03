import os
import unittest
import time
from crawling_gocd.gocd_domain import Organization
from crawling_gocd.crawler import Crawler

class CrawlingPipelineHistoryTest(unittest.TestCase):
    def setUp(self):
        self.orgnization = Organization(
            os.environ["GOCD_SITE"], os.environ["GOCD_USER"], os.environ["GOCD_PASSWORD"])
        self.crawler = Crawler(self.orgnization)

    def test_should_return_pipelines_correctly(self):
        pipelines = self.crawler.getPipelineHistories(
            "accounting-plus-master", time.localtime(1567052779277), time.localtime(1567335377730))
        self.assertEqual(len(pipelines), 16)

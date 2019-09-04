import os
import unittest
import json
from datetime import datetime
from crawling_gocd.gocd_domain import Organization
from crawling_gocd.crawler import Crawler
from unittest.mock import MagicMock


class CrawlerTest(unittest.TestCase):
    def setUp(self):
        self.orgnization = Organization("test.com", "username", "password")
        self.crawler = Crawler(self.orgnization)
        self.filePage1 = "tests/unit/resources/pipeline_history_pg_1.json"
        self.filePage2 = "tests/unit/resources/pipeline_history_pg_2.json"

    def test_generate_pipeline_history_url_correctly(self):
        url = self.crawler.generatePipelineHistoryUrl("go_service", 10)
        self.assertEqual(
            "https://test.com/go/pipelineHistory.json?pipelineName=go_service&start=10", url)

        url = self.crawler.generatePipelineHistoryUrl("go_service", 0)
        self.assertEqual(
            "https://test.com/go/pipelineHistory.json?pipelineName=go_service", url)

    def test_generate_pipeline_history_url_failed(self):
        url = self.crawler.generatePipelineHistoryUrl("go_service", 10)
        self.assertNotEqual(
            "https://test.com/go/pipelineHistory.json?pipelineName=go_service", url)

    def test_should_return_true_when_data_is_over_time(self):
        with open(self.filePage1, 'r') as f:
            page1 = json.load(f)
        pipelines = list(map(lambda x: x["history"], page1["groups"]))
        self.assertTrue(self.crawler.canStop(pipelines[0], datetime.fromtimestamp(1567075172220/1000)))

    def test_should_return_false_when_data_is_not_over_time(self):
        with open(self.filePage1, 'r') as f:
            page1=json.load(f)
        pipelines=list(map(lambda x: x["history"], page1["groups"]))
        self.assertFalse(self.crawler.canStop(
            pipelines[0], datetime.fromtimestamp(1567075172200/1000)))

    def test_should_filter_data_when_data_is_over_time(self):
        with open(self.filePage1, 'r') as f:
            page1=json.load(f)
        pipelines=list(map(lambda x: x["history"], page1["groups"]))
        result=self.crawler.filterPipelinesPerPage(pipelines[0], datetime.fromtimestamp(1567075172220 / 1000), datetime.fromtimestamp(1567335377730/1000))
        self.assertEqual(len(result), 8)

    def test_should_get_pipeline_history_correctly(self):
        def side_effect(arg):
            if arg == "https://test.com/go/pipelineHistory.json?pipelineName=go_service&start=10":
                jsonFile=self.filePage2
            else:
                jsonFile=self.filePage1
            with open(jsonFile, 'r') as f:
                return json.load(f)

        self.crawler.getResource=MagicMock(side_effect=side_effect)
        pipelines=self.crawler.getPipelineHistories("go_service", datetime.fromtimestamp(1567052779277/1000), datetime.fromtimestamp(1567335377730/1000))
        self.assertEqual(len(pipelines), 16)

if __name__ == '__main__':
    unittest.main()

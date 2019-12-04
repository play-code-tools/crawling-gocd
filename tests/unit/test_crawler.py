import os
import unittest
import json
import tests.unit.test_fixture as fixture
from datetime import datetime, timezone
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
        pipelineHistories = fixture.getPipelineHistories(self.filePage1)
        self.assertTrue(self.crawler.canStop(pipelineHistories, datetime(2019, 8, 29, 10, 40, tzinfo=timezone.utc)))

    def test_should_return_false_when_data_is_not_over_time(self):
        pipelineHistories = fixture.getPipelineHistories(self.filePage1)
        self.assertFalse(self.crawler.canStop(pipelineHistories, datetime(2019, 8, 29, 8, 39, tzinfo=timezone.utc)))

    def test_should_filter_data_when_data_is_over_time(self):
        pipelineHistories = fixture.getPipelineHistories(self.filePage1)
        result=self.crawler.filterPipelinesPerPage(pipelineHistories, datetime(2019, 8, 29, 10, 40, tzinfo=timezone.utc))
        self.assertEqual(len(result), 9)

    def test_should_get_pipeline_history_correctly(self):
        def side_effect(arg):
            if arg == "https://test.com/go/pipelineHistory.json?pipelineName=go_service&start=10":
                jsonFile=self.filePage2
            else:
                jsonFile=self.filePage1
            with open(jsonFile, 'r') as f:
                return json.load(f)

        self.crawler.getResource=MagicMock(side_effect=side_effect)
        pipelineHistories=self.crawler.getPipelineHistories("go_service", datetime(2019, 8, 29, 3, 52, tzinfo=timezone.utc), 
            datetime(2019, 9, 2, 4, tzinfo=timezone.utc))
        self.assertEqual(len(pipelineHistories), 18)


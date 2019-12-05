import unittest
import os
import tests.unit.test_fixture as fixture
from unittest.mock import MagicMock, Mock
from crawling_gocd.portal import Portal
from crawling_gocd.outputs import OutputCsv
from crawling_gocd.inputs_parser import InputsParser
from crawling_gocd.gocd_domain import Pipeline
from crawling_gocd.calculate_domain import InputsCalcConfig


class PortalTest(unittest.TestCase):
    def setUp(self):
        os.environ["GOCD_SITE"] = "test.com"
        os.environ["GOCD_USER"] = "test_user"
        os.environ["GOCD_PASSWORD"] = "123456"

        self.portal = Portal()
        self.portal.inputsParser = InputsParser(
            "tests/unit/resources/crawling-gocd.yaml")
        self.portal.crawler.getPipelineHistories = MagicMock(
            return_value=fixture.getPipelineHistories("tests/unit/resources/pipeline_history_pg_1.json"))

    def test_new_crawler_correctly(self):
        self.assertIsNotNone(self.portal.crawler)

    def test_new_crawler_failed(self):
        os.environ.pop("GOCD_SITE", None)
        os.environ.pop("GOCD_USER", None)
        os.environ.pop("GOCD_PASSWORD", None)
        self.assertRaises(KeyError, Portal)

    def test_new_calculator_correctly(self):
        self.assertEqual(len(self.portal.calculator.strategyHandlers), 4)

    def test_new_output_instance_correctly(self):
        self.assertTrue(type(self.portal.output[0]) == OutputCsv)

    def test_get_global_time_range_correctly(self):
        self.assertIsNotNone(self.portal.getGlobalTimeRange())

    def test_crawling_single_pipeline_correctly(self):
        pipeline = Pipeline("test", InputsCalcConfig({}, Mock(), Mock()))
        result = self.portal.crawlingSinglePipeline(pipeline)
        self.assertTrue(len(result.histories) > 0)

    def test_should_call_output_when_serve(self):
        self.portal.output = [Mock()]
        self.portal.serve()
        self.portal.output[0].output.assert_called_once()
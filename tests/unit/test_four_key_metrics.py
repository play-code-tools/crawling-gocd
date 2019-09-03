import unittest
import json
from crawling_gocd.four_key_metrics import DeploymentFrequency
from crawling_gocd.gocd_domain import Pipeline
from crawling_gocd.crawler import CrawlingDataMapper

class DeploymentFrequencyTest(unittest.TestCase):
    def setUp(self):
        self.filePage1 = "tests/unit/resources/pipeline_history_pg_1.json"
        with open(self.filePage1, 'r') as f:
            page1 = json.load(f)
        pipelineHistories = list(map(lambda x: x["history"], page1["groups"]))[0]
        mapper = CrawlingDataMapper()
    
        self.pipeline = Pipeline("go_service", {"qa": ["flyway-qa", "deploy-qa"]})
        self.pipeline.setHistories(mapper.mapPipelineHistory(pipelineHistories))

    def test_should_calculate_deployment_frequency_correctly(self):
        handler = DeploymentFrequency()
        results = handler.calculate([self.pipeline])
        
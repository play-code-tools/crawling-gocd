import unittest
import json
import datetime
import tests.unit.test_fixture as fixture
from crawling_gocd.four_key_metrics import DeploymentFrequency, ChangeFailPercentage, MeanTimeToRestore, ChangeFailPercentage_ignoredContinuousFailed
from crawling_gocd.gocd_domain import Pipeline
from crawling_gocd.crawler import CrawlingDataMapper
from crawling_gocd.calculate_domain import InputsCalcConfig


class DeploymentFrequencyTest(unittest.TestCase):
    def setUp(self):
        self.pipeline = fixture.generatePipeline()

    def test_should_calculate_deployment_frequency_correctly(self):
        handler = DeploymentFrequency()
        results = handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: DeploymentFrequency, groupName: qa, value: 5 }")


class ChangeFailPercentageTest(unittest.TestCase):
    def setUp(self):
        self.pipeline = fixture.generatePipeline()

    def test_should_calculate_change_fail_percentage_correctly(self):
        handler = ChangeFailPercentage()
        results = handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: ChangeFailPercentage, groupName: qa, value: 40.0% }")

class ChangeFailPercentage_ignoredContinuousFailedTest(unittest.TestCase):
    def setUp(self):
        self.pipeline = fixture.generatePipeline()

    def test_should_calculate_change_fail_percentage_correctly(self):
        handler = ChangeFailPercentage_ignoredContinuousFailed()
        results = handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: ChangeFailPercentage_2, groupName: qa, value: 40.0% }")

class MeanTimeToRestoreTest(unittest.TestCase):
    def setUp(self):
        self.pipeline = fixture.generatePipeline()
        self.handler = MeanTimeToRestore()

    def test_should_calculate_mean_time_to_restore_correctly_when_last_history_is_failed(self):
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: MeanTimeToRestore, groupName: qa, value: 837(mins) }")
                    
    def test_should_calculate_mean_time_to_restore_correctly_when_last_history_is_successful(self):
        self.pipeline.calcConfig.endTime = datetime.datetime(2019, 8, 30, 8, 34, tzinfo=datetime.timezone.utc)
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: MeanTimeToRestore, groupName: qa, value: 69(mins) }")

    def test_should_return_NA_when_no_depolyment(self):
        self.pipeline.calcConfig.endTime = datetime.datetime(2019, 8, 29, 8, 34, tzinfo=datetime.timezone.utc)
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: MeanTimeToRestore, groupName: qa, value: N/A }")
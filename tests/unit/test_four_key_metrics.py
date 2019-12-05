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
        self.handler = ChangeFailPercentage()

    def test_should_calculate_change_fail_percentage_correctly(self):
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: ChangeFailPercentage, groupName: qa, value: 40.0% }")

    def test_should_return_NA_when_zero_deployment(self):
        self.pipeline.calcConfig.endTime = datetime.datetime(2019, 8, 29, 8, 34, tzinfo=datetime.timezone.utc)
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: ChangeFailPercentage, groupName: qa, value: N/A }")

class ChangeFailPercentage_ignoredContinuousFailedTest(unittest.TestCase):
    def setUp(self):
        self.pipeline = fixture.generatePipeline()
        self.handler = ChangeFailPercentage_ignoredContinuousFailed()

    def test_should_calculate_change_fail_percentage_correctly(self):
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: ChangeFailPercentage_2, groupName: qa, value: 40.0% }")

    def test_return_NA_when_zero_deployment(self):
        self.pipeline.calcConfig.endTime = datetime.datetime(2019, 8, 29, 8, 34, tzinfo=datetime.timezone.utc)
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: ChangeFailPercentage_2, groupName: qa, value: N/A }")

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

    def test_should_calculate_mean_time_to_restore_when_newest_is_failed(self):
        self.pipeline.histories.pop(-1)
        self.pipeline.calcConfig.endTime = datetime.datetime(2019, 9, 2, tzinfo=datetime.timezone.utc)
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: MeanTimeToRestore, groupName: qa, value: 1229(mins) }")
    
    def test_should_return_NA_when_zero_depolyment(self):
        self.pipeline.calcConfig.endTime = datetime.datetime(2019, 8, 29, 8, 34, tzinfo=datetime.timezone.utc)
        results = self.handler.calculate([self.pipeline], [])
        self.assertEqual("".join(str(x) for x in results),
                         "{ pipelineName: go_service, metricsName: MeanTimeToRestore, groupName: qa, value: N/A }")
import os
from crawling_gocd.inputs_parser import InputsParser
from crawling_gocd.gocd_domain import Organization 
from crawling_gocd.crawler import Crawler, CrawlingDataMapper
from crawling_gocd.calculator import Calculator
from crawling_gocd.four_key_metrics import DeploymentFrequency, ChangeFailPercentage, MeanTimeToRestore


class Portal:
    def work(self):
        inputPipelines = InputsParser("inputs.yaml").parse()
        orgnization = Organization(os.environ["GOCD_SITE"], os.environ["GOCD_USER"], os.environ["GOCD_PASSWORD"])
        crawler = Crawler(orgnization)
        pipelineWithFullData = list(map(lambda pipeline: self.crawlingSinglePipeline(pipeline, crawler), inputPipelines))

        calculator = self.assembleCalculator()
        results = calculator.work(pipelineWithFullData, [])
        print("==============Results start===================")
        print("\n".join(str(x) for x in results))
        print("==============Results end=====================")

    def crawlingSinglePipeline(self, pipeline, crawler):
        mapper = CrawlingDataMapper()
        histories = crawler.getPipelineHistories(pipeline.name, pipeline.calcConfig.startTime, pipeline.calcConfig.endTime)
        pipeline.histories = mapper.mapPipelineHistory(histories)
        return pipeline
    
    def assembleCalculator(self):
        deploymentFrequencyHandler = DeploymentFrequency()
        changeFailPercentage = ChangeFailPercentage()
        meanTimeToRestore = MeanTimeToRestore()
        return Calculator([deploymentFrequencyHandler, changeFailPercentage, meanTimeToRestore])
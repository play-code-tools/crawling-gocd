from crawling_gocd.inputs_parser import InputsParser
from crawling_gocd.gocd_domain import Organization 
from crawling_gocd.crawler import Crawler, CrawlingDataMapper
from crawling_gocd.calculator import Calculator


class portal:
    def work(self):
        inputPipelines = InputsParser("inputs.yaml").parse()
        orgnization = Organization("test.com", "username", "password")
        crawler = Crawler(orgnization)
        pipelineWithFullData = list(map(lambda pipeline: self.crawlingSinglePipeline(pipeline, crawler), inputPipelines))
        

    def crawlingSinglePipeline(self, pipeline, crawler):
        mapper = CrawlingDataMapper()
        histories = crawler.getPipelineHistories(pipeline.pipelineName, pipeline.calcConfig.startTime, pipeline.calcConfig.endTime)
        pipeline.histories = mapper.mapPipelineHistory(histories)
        return pipeline
    
    def assembleCalculator(self):
        Calculator()
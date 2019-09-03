from crawling_gocd.inputs_parser import InputsParser
from crawling_gocd.gocd_domain import Organization 
from crawling_gocd.crawler import Crawler, CrawlingDataMapper


class portal:
    def work(self):
        inputPipelines = InputsParser("inputs.yaml").parse()

        
        
        crawler.getPipelineHistory()

    def getPipelineHistoriesByCrawler(self, inputPipelines):
        orgnization = Organization("test.com", "username", "password")
        crawler = Crawler(orgnization)
        mapper = CrawlingDataMapper()
        list(map(lambda pipeline: mapper.mapPipelineHistory(crawler.getPipelineHistory(pipeline.pipelineName, )), inputPipelines))

        crawler.getPipelineHistory()
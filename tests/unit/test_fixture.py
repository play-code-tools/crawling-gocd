import json
import itertools
import datetime
from crawling_gocd.crawler import CrawlingDataMapper
from crawling_gocd.gocd_domain import Pipeline
from crawling_gocd.calculate_domain import InputsCalcConfig


def getPipelineHistories(filePath):
    with open(filePath, 'r') as f:
        page1 = json.load(f)
    pipelineHistoriesList = list(
    map(lambda x: x["history"], page1["groups"]))
    return list(itertools.chain(*pipelineHistoriesList))

def generatePipeline():
    filePage1 = "tests/unit/resources/pipeline_history_pg_1.json"
    pipelineHistories = getPipelineHistories(filePage1)
    mapper = CrawlingDataMapper()

    pipeline = Pipeline("go_service", InputsCalcConfig({"qa": ["flyway-qa", "deploy-qa"]}, datetime.datetime(1970, 1, 1), datetime.datetime.now()))
    pipeline.setHistories(mapper.mapPipelineHistory(pipelineHistories))
    return pipeline

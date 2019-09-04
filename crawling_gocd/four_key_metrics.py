from crawling_gocd.calculate_domain import CalculateStrategyHandler, Result

class DeploymentFrequency(CalculateStrategyHandler):
    metrics_name = "Deployment Frequency"
    
    def calculate(self, pipelines, results = []):
        for pipeline in pipelines:
            self.__workForSinglePipeline(pipeline, results)
        return results

    def __workForSinglePipeline(self, pipeline, results):
        for groupedStage in pipeline.calcConfig.groupedStages.items():
            value = self.__workForSingleGroupedStage(pipeline.histories, groupedStage[1])
            results.append(Result(pipeline.name, DeploymentFrequency.metrics_name, groupedStage[0], value))
    
    def __workForSingleGroupedStage(self, pipelineHistories, stageNames):
        return len(list(filter(lambda history: history.hasStatusInStages(stageNames), pipelineHistories)))
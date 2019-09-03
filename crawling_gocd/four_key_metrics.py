from crawling_gocd.calculate_domain import CalculateStrategyHandle, Result

class DeploymentFrequency(CalculateStrategyHandle):
    metrics_name = "Deployment Frequency"
    
    def calculate(self, pipelines, results = []):
        for pipeline in pipelines:
            results.append(self.__workForSinglePipeline(pipeline))
        return results

    def __workForSinglePipeline(self, pipeline):
        for groupedStage in pipeline.calcConfig.items():
            value = self.__workForSingleGroupedStage(pipeline.histories, groupedStage)
            print("===>", value)
            return Result(pipeline.name, metrics_name, groupedStage[0], value)
    
    def __workForSingleGroupedStage(self, pipelineHistories, groupedStage):
        for history in pipelineHistories:
            for stage in history.stages:
                if(stage.name in groupedStage[1]):
        return len(list(filter(lambda history: history.stages in groupedStage[1], pipelineHistories)))
from crawling_gocd.calculate_domain import CalculateStrategyHandler, Result

class CalculateStrategyHandlerBase(CalculateStrategyHandler):
    def calculate(self, pipelines, results):
        for pipeline in pipelines:
            self.calculateSingle(pipeline, results)
        return results

    def calculateSingle(self, pipeline, results):
        for groupedStage in pipeline.calcConfig.groupedStages.items():
            value = self.valueOfSingleGroupedStage(pipeline.histories, groupedStage[1])
            results.append(Result(pipeline.name, self.getMetricName(), groupedStage[0], value))
    
    def getMetricName(self):
        return ""

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames):
        return 0


class DeploymentFrequency(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "Deployment Frequency"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames):
        return len(list(filter(lambda history: history.hasStatusInStages(stageNames), pipelineHistories)))

class ChangeFailPercentage(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "Change Fail Percentage"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames):
        runCount = len(list(filter(lambda history: history.hasStatusInStages(stageNames), pipelineHistories)))
        failedCount = len(list(filter(lambda history: history.hasFailedInStages(stageNames), pipelineHistories)))

        if runCount == 0 and failedCount == 0:
            return "0"

        return "{:.1%}".format(failedCount / runCount)

class MeanTimeToRestore(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "Mean Time To Restore"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames):
        restoreTotalTime, failedCount, latestFailedScheduled = 0, 0, 0

        pipelineHistories.sort(key=lambda history: history.scheduledTimestamp)
        for history in pipelineHistories:
            if history.hasFailedInStages(stageNames) and latestFailedScheduled == 0:
                failedCount += 1
                latestFailedScheduled = history.scheduledTimestamp

            if history.allPassedInStages(stageNames) and latestFailedScheduled != 0:
                restoreTotalTime += history.scheduledTimestamp - latestFailedScheduled
                latestFailedScheduled = 0
        
        if latestFailedScheduled != 0 and failedCount > 0:
            failedCount -= 1

        if failedCount == 0:
            return 0

        return "%s(mins)" % round(restoreTotalTime / failedCount / 1000 / 60)


    

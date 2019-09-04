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
        return "{:.1%}".format(failedCount / runCount)

class MeanTimeToRestore(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "Mean Time To Restore"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames):
        totalTime, count, latestFailedScheduled = 0, 0, 0

        pipelineHistories.sort(key=lambda history: history.scheduledTimestamp)
        for history in pipelineHistories:
            if history.hasFailedInStages(stageNames) and latestFailedScheduled == 0:
                count += 1
                latestFailedScheduled = history.scheduledTimestamp

            if history.allPassedInStages(stageNames) and latestFailedScheduled != 0:
                totalTime += history.scheduledTimestamp - latestFailedScheduled
                latestFailedScheduled = 0
        
        if latestFailedScheduled != 0 and count > 0:
            count -= 1

        if count == 0:
            return 0

        return "%s(mins)" % round(totalTime / count / 1000 / 60)


    

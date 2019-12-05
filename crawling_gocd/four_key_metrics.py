import abc
from datetime import datetime
from crawling_gocd.calculate_domain import CalculateStrategyHandler, Result

class CalculateStrategyHandlerBase(CalculateStrategyHandler):
    def calculate(self, pipelines, results):
        for pipeline in pipelines:
            self.calculateSingle(pipeline, results)
        return results

    def calculateSingle(self, pipeline, results):
        for groupedStage in pipeline.calcConfig.groupedStages.items():
            value = self.valueOfSingleGroupedStage(
                pipeline.histories, groupedStage[1], pipeline.calcConfig.startTime, pipeline.calcConfig.endTime)
            results.append(
                Result(pipeline.name, self.getMetricName(), groupedStage[0], value))

    @abc.abstractmethod
    def getMetricName(self):
        pass

    @abc.abstractmethod
    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames, startTime, endTime):
        pass

    def filterByTimeRange(self, pipelineHistories, startTime, endTime):
        return list(filter(lambda x: datetime.timestamp(startTime) <= (int(x.scheduledTimestamp) / 1000) <= datetime.timestamp(endTime), 
            pipelineHistories))

class DeploymentFrequency(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "DeploymentFrequency"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames, startTime, endTime):
        filteredHistories = self.filterByTimeRange(pipelineHistories, startTime, endTime)
        return len(list(filter(lambda history: history.hasStatusInStages(stageNames), filteredHistories)))

class ChangeFailPercentage(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "ChangeFailPercentage"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames, startTime, endTime):
        filteredHistories = self.filterByTimeRange(pipelineHistories, startTime, endTime)

        runCount = len(list(filter(
            lambda history: history.hasStatusInStages(stageNames), filteredHistories)))
        failedCount = len(list(filter(
            lambda history: history.hasFailedInStages(stageNames), filteredHistories)))

        if runCount == 0:
            return "N/A"

        return "{:.1%}".format(failedCount / runCount)

class ChangeFailPercentage_ignoredContinuousFailed(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "ChangeFailPercentage_2"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames, startTime, endTime):
        filteredHistories = self.filterByTimeRange(pipelineHistories, startTime, endTime)
        runCount = len(list(filter(
            lambda history: history.hasStatusInStages(stageNames), filteredHistories)))

        filteredHistories.sort(key=lambda history: history.label)
        failedCount, lastIsFailed = 0, False
        for history in filteredHistories:
            if history.hasFailedInStages(stageNames) and lastIsFailed == False:
                failedCount += 1
                lastIsFailed = True

            if history.allPassedInStages(stageNames) and lastIsFailed == True:
                lastIsFailed = False

        if runCount == 0:
            return "N/A"

        return "{:.1%}".format(failedCount / runCount)


class MeanTimeToRestore(CalculateStrategyHandlerBase):
    def getMetricName(self):
        return "MeanTimeToRestore"

    def valueOfSingleGroupedStage(self, pipelineHistories, stageNames, startTime, endTime):
        filteredHistories = self.filterByTimeRangeAndEndBySuccessfulStatus(pipelineHistories, stageNames, startTime, endTime)

        restoreTotalTime, failedCount, latestFailedScheduled = 0, 0, 0
        filteredHistories.sort(key=lambda history: history.scheduledTimestamp)
        for history in filteredHistories:
            if history.hasFailedInStages(stageNames) and latestFailedScheduled == 0:
                failedCount += 1
                latestFailedScheduled = history.scheduledTimestamp

            if history.allPassedInStages(stageNames) and latestFailedScheduled != 0:
                restoreTotalTime += history.scheduledTimestamp - latestFailedScheduled
                latestFailedScheduled = 0

        if latestFailedScheduled != 0 and failedCount > 0:
            restoreTotalTime += datetime.timestamp(endTime) * 1000 - latestFailedScheduled

        if failedCount == 0:
            return "N/A"

        return "%s(mins)" % round(restoreTotalTime / failedCount / 1000 / 60)

    def filterByTimeRangeAndEndBySuccessfulStatus(self, pipelineHistories, stageNames, startTime, endTime):
        histories = sorted((h for h in pipelineHistories if h.hasFailedInStages(stageNames) or h.allPassedInStages(stageNames)), key = lambda history: int(history.label))
        historiesInTimeRange = self.filterByTimeRange(histories, startTime, endTime)
        if len(historiesInTimeRange) == 0:
            return []

        lastHistory = historiesInTimeRange[-1]
        if lastHistory.allPassedInStages(stageNames):
            return historiesInTimeRange
        else:
            allFixedList = list(filter(lambda h: int(h.label) > int(lastHistory.label) and h.allPassedInStages(stageNames), histories))
            if len(allFixedList) == 0:
                return historiesInTimeRange

            lastFixedPipeline = histories[-1]
            historiesInTimeRange.append(lastFixedPipeline)
            return historiesInTimeRange

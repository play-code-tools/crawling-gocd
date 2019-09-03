
class InputsCalcConfig:
    def __init__(self, groupedStages, startTime, endTime):
        self.groupedStages = groupedStages
        self.startTime = startTime
        self.endTime = endTime

    def __str__(self):
        return "{ groupedStages: %s, startTime: %s, endTime: %s }" % (str(self.groupedStages), str(self.startTime), str(self.endTime))

class CalculateStrategyHandle:
    def calculate(self, pipelines):
        pass

class Result:
    def __init__(self, pipelineName, metricsName, groupName, value):
        self.pipelineName = pipelineName
        self.metricsName = metricsName
        self.groupName = groupName
        self.value = value
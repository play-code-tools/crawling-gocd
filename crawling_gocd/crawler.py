import time
from operator import attrgetter
from datetime import datetime
from requests_html import HTMLSession


class Crawler:
    def __init__(self, organization):
        self.path = "./data"
        self.organization = organization
        self.session = HTMLSession()
        self.session.headers.update(
            {"Authorization": self.organization.getBasicAuth()})

    def getResource(self, url):
        return self.session.get(url=url).json()

    def generatePipelineHistoryUrl(self, pipelineName, start=0):
        url = "https://{}/go/pipelineHistory.json?pipelineName={}".format(
            self.organization.site, pipelineName)
        if start != 0:
            url = url + "&start={}".format(start)
        return url

    def getPipelineHistory(self, pipelineName, startTime, endTime):
        if startTime > endTime:
            return []
        offset, data = 0, []
        while True:
            url = self.generatePipelineHistoryUrl(pipelineName, offset)
            print("get url {}".format(url))
            try:
                ret = self.getResource(url)
                pipelines = list(map(lambda x: x["history"], ret["groups"]))[0]
                if len(pipelines) == 0:
                    break

                data = data + \
                    self.filterPipelinesPerPage(
                        pipelines, startTime, endTime)

                if self.canStop(pipelines, startTime):
                    break

                offset = ret["start"] + ret["perPage"]
            except:
                print("failed {}".format(url))
                break
        return data

    def filterPipelinesPerPage(self, pipelines, startTime, endTime):
        return list(filter(lambda x: (time.mktime(startTime) <= int(x["scheduled_timestamp"]) <= time.mktime(endTime)), pipelines))

    def canStop(self, pipelines, startTime):
        scheduledTimestatmps = list(map(lambda x: int(x["scheduled_timestamp"]), pipelines))
        return min(scheduledTimestatmps) < time.mktime(startTime)

    

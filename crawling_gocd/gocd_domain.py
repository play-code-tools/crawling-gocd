import base64


class Organization:
    def __init__(self, site, user, token):
        self.site = site
        self.user = user
        self.token = token

    def getBasicAuth(self):
        return "Basic {}".format(base64.b64encode((self.user + ":" + self.token).encode('utf-8')).decode())


class Pipeline:
    def __init__(self, name, calcConfig):
        self.name = name
        self.calcConfig = calcConfig

    def __str__(self):
        return "{ name: %s, calcConfig: %s }" % (self.name, str(self.calcConfig))
    
    def setHistories(self, histories):
        self.histories = histories
    
class PipelineHistory:
    def __init__(self, label, scheduledTimestamp, stages):
        self.label = label
        self.scheduledTimestamp = scheduledTimestamp
        self.stages = stages

    def __str__(self):
        return "{ label: %s, scheduledTimestamp: %s, stages: %s }" % (self.label, str(self.scheduledTimestamp), str(", ".join(str(stage) for stage in self.stages)))


class StageHistory:
    def __init__(self, oid, name, status):
        self.id = oid
        self.name = name
        self.status = status

    def __str__(self):
        return "{ id: %s, name: %s, status: %s}" % (self.id, self.name, self.status)

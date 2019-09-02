import base64

class Organization:
    def __init__(self,site,user,token):
        self.site = site
        self.user = user
        self.token = token

    def getBasicAuth(self):
        return "Basic {}".format(base64.b64encode((self.user +":"+ self.token).encode('utf-8')).decode())

class Pipeline:
    def __init__(self, name):
        self.name = name

class PipelineHistory:
    def __init__(self, pipeline, label, scheduledTimestamp, stages):
        self.pipeline = pipeline
        self.label = label
        self.scheduledTimestamp = scheduledTimestamp
        self.stages = stages

class Stage:
    def __init__(self, oid, name, status):
        self.id = oid
        self.name = name
        self.status = status


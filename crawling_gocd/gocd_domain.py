import base64

class Organization:
    def __init__(self,site,user,token):
        self.site = site
        self.user = user
        self.token = token

    def getBasicAuth(self):
        return "Basic {}".format(base64.b64encode((self.user +":"+ self.token).encode('utf-8')).decode())

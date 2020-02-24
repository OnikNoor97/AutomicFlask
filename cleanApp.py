from AutomicLogin import AutomicLogin
import json
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# Clean Environments - The purpose of this is to ensure that all Applications are updated to prod including branch
url = "http://evsvraut2018.eviivo.local:8090/api/data/v1"

class cleanApp(AutomicLogin):

    def __init__(self, AutomicLogin):
        self.AutomicLogin = AutomicLogin

    def get_application_id(self, AutomicLogin, applicationName):
        r = requests.get(url+"/applications?max_results=100", auth=HTTPBasicAuth("100/"+AutomicLogin.username+"/EVIIVO" , AutomicLogin.password) )
        jsonParse = r.json()
        for i in jsonParse['data']:
            if i['archived'] == False and i['name'] == applicationName:
                return i['id']

    def getProfiles(self, AutomicLogin, id): #Without Production
        r = requests.get(url+"/applications/"+str(id)+"/profiles?max_results=100", auth=HTTPBasicAuth("100/"+AutomicLogin.username+"/EVIIVO" , AutomicLogin.password) )
        jsonParse = r.json()
        profiles = []
        for i in jsonParse['data']:
            if i['archived'] == False and ("QA" in i["name"]) or ("DRYRUN" in i["name"]) or ("STAGE" in i["name"]) or ("DEMO" in i["name"]):
                profiles.append(i['name'])
        return profiles

    def view_last_deployed_version(self, AutomicLogin, app, id, profile):
        r = requests.get(url+"/executions?application.name="+app+"&max_results=1000&deployment_profile.name="+profile+"&status=Finished", auth=HTTPBasicAuth("100/"+AutomicLogin.username+"/EVIIVO" , AutomicLogin.password) )
        deployList = []
        jsonParse = r.json()
        try:
            for i in jsonParse['data']:
                deployList.append(i['package']['name'])
            return deployList[-1]
        except: # except for new applications
            deployList.append("never")
            return deployList[0]

    def post_deployment(self, AutomicLogin, application, package, profile):
        endpoint = url+"/executions"
        payload =   {
                        'application': application,
                        'package': package,
                        'deployment_profile': profile,
                        'workflow' : 'Deployment'
                    }
        headers = {'content-type': 'application/json'}
        r = requests.post(endpoint, auth=HTTPBasicAuth("100/"+AutomicLogin.username+"/EVIIVO" , AutomicLogin.password), data=json.dumps(payload), headers=headers)
        if (r.status_code != 201):
            print("Deployment request unsuccessful for \nApplication: "+application + "\nPackage: "+ package + "\nProfile: " + profile)
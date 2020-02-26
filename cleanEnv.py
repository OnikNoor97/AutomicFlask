from AutomicLogin import AutomicLogin
import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

url = "http://evsvraut2018.eviivo.local:8090/api/data/v1"

class cleanEnv(AutomicLogin):

    def __init__(self, AutomicLogin):
        self.AutomicLogin = AutomicLogin

    def get_applications(self, env):
        data = requests.get('https://qastatus.eviivo.com/compare/PROD?environment='+env)
        soup = BeautifulSoup(data.text, 'html.parser')

        versionArray = []
        for tr in soup.find_all('tr'):
            value = [td.text.rstrip(" \nClean up app").strip() for td in tr.find_all('td')] # Gets rid of Clean up app button content
            if '' not in value:
                versionArray.append(value)
        versionArray.pop(0) # Gets rid of the key content
        cleanArray = [x for x in versionArray if x != []] # Gets rid of empty array to avoid index errors
        
        # 0 is application name
        # 1 is PROD version
        # 2 is env version

        return cleanArray
    
    def getProfile(self, AutomicLogin, id, env): #Without Production
        r = requests.get(url+"/applications/"+str(id)+"/profiles?max_results=100", auth=HTTPBasicAuth("100/"+AutomicLogin.username+"/EVIIVO" , AutomicLogin.password) )
        jsonParse = r.json()
        profile = ""
        for i in jsonParse['data']:
            if i['archived'] == False and (env in i["name"]):
                profile = i['name']
        return profile

    def post_deployment(self, AutomicLogin, applications, package, profile):
        endpoint = url+"/executions"
        for application in applications:
            payload = {
                        'application': application,
                        'package': package,
                        'deployment_profile': profile,
                        'workflow' : 'Deployment'
                        }
        headers = {'content-type': 'application/json'}
        r = requests.post(endpoint, auth=HTTPBasicAuth("100/"+AutomicLogin.username+"/EVIIVO" , AutomicLogin.password), data= json.dumps(payload), headers=headers)
        if (r.status_code != 201):
            print("Deployment request unsuccessful for \nApplication: "+application + "\nPackage: "+ package + "\nProfile: " + profile)

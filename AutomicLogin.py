import json
import requests
from requests.auth import HTTPBasicAuth

class AutomicLogin:
        
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername(self):
        return "100/"+self.username+"/EVIIVO"

    def getPassword(self):
        return self.password    

    # Message first, then success boolean
    def testLogin(self):
        url = "http://evsvraut2018.eviivo.local:8090/api/data/v1"
        r = requests.get(url+"/applications?max_results=1", auth=HTTPBasicAuth("100/"+self.username+"/EVIIVO" , self.password) )
        if(r.status_code == 200):
            return "Login Successful!"
        elif(r.status_code == 401):
            return "Incorrect username or password!"
        else:
            return "Something went wrong! Status code: " + str(r.status_code)

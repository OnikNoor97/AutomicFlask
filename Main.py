from Validator import Validator
from AutomicLogin import AutomicLogin
from cleanEnv import cleanEnv
from cleanApp import cleanApp

# Deploying first, then Deployed (In the Parameters)

v = Validator()
user = AutomicLogin("onoor", "OnikNoor")

def cleanApplication(app, deploying):
    ca = cleanApp(user)
    id = ca.get_application_id(user,app)
    profiles = ca.getProfiles(user, id)

    for profile in profiles:
        deployed = ca.view_last_deployed_version(user, app, id, profile)
        checker = v.ignoreBranch(deploying, deployed)
        if(checker):
            ca.post_deployment(user, app, deploying, profile)
            print("Deploying: " + profile)
        else:
            print("Not deploying on " + profile)

cleanApplication("AirbnbListingFeed", "4.10.1.108")
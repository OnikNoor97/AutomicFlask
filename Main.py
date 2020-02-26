from Validator import Validator
from AutomicLogin import AutomicLogin
from cleanEnv import cleanEnv
from cleanApp import cleanApp

# Deploying first, then Deployed (In the Parameters)

v = Validator()
user = AutomicLogin("onoor", "OnikNoor")

def cleanApplication(app, deploying): # Tested (/)
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

#cleanApplication("AirbnbListingFeed", "4.10.1.108")

def cleanEnvironment(env):
    ce = cleanEnv(user)
    apps = ce.get_versions(env)
    for app in apps:

        # app[0] is application name
        # app[1] is PROD version
        # app[2] is env version

        checker = v.overrideBranch(app[1], app[2])
        if(checker):
            appId = ce.get_application_id(user, app[0])
            profile = ce.getProfile(user, appId, env)
            #print("Deploy for " + app[0])
            ce.post_deployment(user, app, app[1], profile)
        else:
            print("Not deploying " + app[0])

cleanEnvironment("STAGE1")
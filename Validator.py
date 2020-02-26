import re

class Validator:

    # This function should return false if a branch version is detected, this should be for cleaning environments
    def overrideBranch(self, deployingString, deployedString): # Tested (/)

        deployed = deployedString.split(".")
        deploying = deployingString.split(".")
        c = len(deployed) - len(deploying)
        i = 0
        checker = False
        
        if (c > 0):
            deploying.extend('0' * abs(c))
        elif(c < 0):
            deployed.extend('0' * abs(c))

        if len(deployed) == len(deploying):
            while (i < len(deployed)):
                if "-" in deployed[i]:
                    checker = True
                    break
                if ("N/A") in deployed[i]: # N/A will be ignored, manual deployed for new applications will need to be done
                    checker = False
                    break
                if  int(deployed[i]) < int(deploying[i]):
                    checker = True
                i += 1
        else:
            checker = False
        return checker


    # This function should return true if a branch version is not detected, this should be for cleaning applications
    def ignoreBranch(self, deployingString, deployedString): #Tested (/)    
        
        deployed = deployedString.split(".")
        deploying = deployingString.split(".")
        c = len(deployed) - len(deploying)
        checker = False
        
        if (c > 0):
            deploying.extend('0' * abs(c))
        elif(c < 0):
            deployed.extend('0' * abs(c))

        i = 0
        if len(deployed) == len(deploying):
            while (i < len(deployed)):
                if "-" in deployed[i]:
                    checker = False
                    break
                if ("N/A") in deployed[i]: # N/A will be ignored, manual deployed for new applications will need to be done
                    checker = False
                    break
                if  int(deployed[i]) < int(deploying[i]):
                    checker = True
                i += 1
        else:
            checker = False
        return checker


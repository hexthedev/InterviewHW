import requests
import sys

"""
Helper functions used by tests
"""
args = sys.argv
lenargs = len(args)

# load the config json and determine host
defaultServerIp = "localhost" 
defaultServerPort = "5000" 

serverIp = defaultServerIp if lenargs < 3 else args[1]
serverPort = defaultServerPort if lenargs < 3 else args[2]

url = f"http://{serverIp}:{serverPort}/vehicleStatus/query"

def constructAndSendRequest(url, submitDate, purchaseDate, odometer, isOverhauled):
  return requests.post(url = url, json = {
    "submitDate": submitDate,
    "purchaseDate": purchaseDate,
    "odometer": odometer,
    "isOverhauled": isOverhauled
  })

def checkJsonOutput(json, isTimeRelatedMaintenance = False, isDistanceRelatedMaintenance = False, isScrapped = False):
  if json["isTimeRelatedMaintenance"] != isTimeRelatedMaintenance:
    return False
  if json["isDistanceRelatedMaintenance"] != isDistanceRelatedMaintenance:
    return False
  if json["isScrapped"] != isScrapped:
    return False
  return True

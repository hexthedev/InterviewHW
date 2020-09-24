"""
Helper functions used by tests
"""
import requests

url = "http://localhost:5000/vehicleStatus/query"

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
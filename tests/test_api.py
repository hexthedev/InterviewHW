import sys
import requests

args = sys.argv
lenargs = len(args)

# load the config json and determine host
defaultServerIp = "localhost" 
defaultServerPort = "5000" 

serverIp = defaultServerIp if lenargs < 3 else args[1]
serverPort = defaultServerPort if lenargs < 3 else args[2]

url = f"http://{serverIp}:{serverPort}/vehicleStatus/query"

# Helpers
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

# Bad Request Tests
def test_badRequest_withoutJson():
  res = requests.post(url = url)
  assert res.status_code == 400

def test_badRequest_badJson():
  res = requests.post(url = url, json = {"bad" : "bad"})
  assert res.status_code == 400

def test_badRequest_submitDateBadFormat():
  res = constructAndSendRequest(url, "28/10/1992", "2010/10/28", 10, True)
  assert res.status_code == 400

def test_badRequest_purchaseDateBadFormat():
  res = constructAndSendRequest(url, "2010/10/28", "28/10/1992", 10, True)
  assert res.status_code == 400

def test_badRequest_odometerNotInt():
  res = constructAndSendRequest(url, "2010/10/28", "2010/10/28", "Test", True)
  assert res.status_code == 400

def test_badRequest_isOverhauledNotBool():
  res = constructAndSendRequest(url, "2010/10/28", "2010/10/28", 10, "Test")
  assert res.status_code == 400

# Should Scrap Tests
def test_shouldScrap_0MonthDifference():
  res = constructAndSendRequest(url, "1998/06/06", "1992/06/06", 10, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isScrapped= True)

def test_shouldScrap_0MonthDifference_Overhaul():
  res = constructAndSendRequest(url, "1995/06/06", "1992/06/06", 10, True)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isScrapped= True)
  
def test_shouldScrap_1MonthDifference():
  res = constructAndSendRequest(url, "1998/05/06", "1992/06/06", 10, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isScrapped= True)

def test_shouldScrap_1MonthDifference_EndOfYearCase():
  res = constructAndSendRequest(url, "1998/12/12", "1993/01/01", 10, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isScrapped= True)

def test_shouldScrap_2MonthDifference():
  res = constructAndSendRequest(url, "1998/04/06", "1992/06/06", 10, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json())

# Distance Maintenance Tests
def test_distanceMaintenance_500untilMaintenance():
  res = constructAndSendRequest(url, "1992/01/01", "1992/01/01", 9500, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isDistanceRelatedMaintenance=True)

def test_distanceMaintenance_501untilMaintenance():
  res = constructAndSendRequest(url, "1992/01/01", "1992/01/01", 9499, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json())

def test_distanceMaintenance_0odometer():
  res = constructAndSendRequest(url, "1992/01/01", "1992/01/01", 0, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json())

#  Maintenance Tests
def test_timeMaintenence_Under3_MonthBefore():
  res = constructAndSendRequest(url, "1992/12/01", "1992/01/01", 0, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance=True)

def test_timeMaintenence_Under3_MonthOf():
  res = constructAndSendRequest(url, "1993/01/01", "1992/01/01", 0, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance=True)

def test_timeMaintenence_Over3_MonthBefore():
  res = constructAndSendRequest(url, "1995/06/01", "1992/01/01", 0, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance=True)

def test_timeMaintenence_Over3_MonthOf():
  res = constructAndSendRequest(url, "1995/07/01", "1992/01/01", 0, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance=True)

def test_timeMaintenence_Overhaul():
  res = constructAndSendRequest(url, "1992/03/01", "1992/01/01", 0, True)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance=True)
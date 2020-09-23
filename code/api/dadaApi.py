from flask import Flask, json, request, Response
import datetime

api = Flask(__name__)

# Input validation
badInputResponse = Response(status=400)

def validateIsBool(x):
  if not isinstance(x, (bool)):
    raise ValueError("Expected a bool")

expectedKeys = {
  "submitDate" : lambda x : datetime.datetime.strptime(x, "%Y/%m/%d"),
  "purchaseDate" : lambda x : datetime.datetime.strptime(x, "%Y/%m/%d"),
  "odometer" : int,
  "isOverhauled": validateIsBool
}

# Constants (but not really in python)
nonOverhaluedScrapThreshold = 2190
overhauledScrapThreshold = 1095

kmsPerDistMaintainence = 10000
distMaintenanceNotifyThreshold = 500

timeMainUnder3YearThreshold = 12
timeMainOver3YearThreshold = 6
timeMainOverhaulThreshold = 3

# Helper Functions
def validateJson(json):
  """Makes sure json contains required keys and their values are correctly formatted"""
  if json is None:
    return False

  # validate json, making sure it has the right keys
  # and keys have the correct format
  for k, v in expectedKeys.items():
    
    if k not in json:
      return False
    
    try:
      v(json[k])
    except ValueError:
      return False

  return True

def constructJson(isTimeRelatedMaintenance = False, isDistanceRelatedMaintenance = False, isScrapped =False):
  """Helper to easily construct response json objects"""

  return {
    "isTimeRelatedMaintenance": isTimeRelatedMaintenance,
    "isDistanceRelatedMaintenance": isDistanceRelatedMaintenance,
    "isScrapped": isScrapped
  }

# Api checker functions
def checkShouldScrap(purchaseDate, submitDate, isOverhauled): 
  """
  Tests if conditions are met such that scrapping is required 
  (or should be notified). A scrap notification should occur 1 month before
  the scrap threshold. The threshold for overhauled cars is 1095 days from purchase date.
  For non-overhauled cars it is 2190 days
  """
  scrapThreshold =  overhauledScrapThreshold if isOverhauled else nonOverhaluedScrapThreshold
  
  scrapDate = purchaseDate + datetime.timedelta(days = scrapThreshold)

  if scrapDate.year - submitDate.year <= 1:
    # if scrap month a year ahead, add 12 months so it's always larger
    offsetScrapMonth = scrapDate.month if scrapDate.year == submitDate.year else scrapDate.month + 12

    # if submitted within 1 month of scrapDate, then needs scrapping
    if offsetScrapMonth - submitDate.month <= 1:
      return True

  return False

def checkShouldDistanceMaintenance(odometer): 
  """
  Tests if conditions are met such that distance maintenance is required. This is every
  10000 km. Notifications should occur 500 km before. 
  """
  kmsSinceMaintainence = odometer % kmsPerDistMaintainence
  
  if kmsPerDistMaintainence - kmsSinceMaintainence <= distMaintenanceNotifyThreshold:
    return True

  return False

def checkShouldTimeMaintenance(purchaseDate, submitDate, isOverhauled): 
  """
  Tests if conditions are met such that time maintenance is required. This is every 6 months for 12 months for cars < 3 years, 6 months for cars over or >= 3 year, or 3 months for overhauled cars
  """
  print(submitDate.year)
  print(purchaseDate.year)
  
  purchaseSubmitYearDelta = submitDate.year - purchaseDate.year
  
  if isOverhauled:
    timeMainThreshold = timeMainOverhaulThreshold
  elif purchaseSubmitYearDelta < 3:
    timeMainThreshold = timeMainUnder3YearThreshold
  else:
    timeMainThreshold = timeMainOver3YearThreshold

  yearMonthOffset = submitDate.month - purchaseDate.month
  purchaseSubmitMonthDelta = purchaseSubmitYearDelta * 12 + yearMonthOffset
  monthCycleMod = purchaseSubmitMonthDelta % timeMainThreshold

  print(purchaseSubmitYearDelta)
  print(timeMainThreshold)
  print(yearMonthOffset)
  print(purchaseSubmitMonthDelta)
  print(monthCycleMod)

  if yearMonthOffset == 0 and purchaseSubmitYearDelta == 0:
      return False

  if monthCycleMod == 0 or (timeMainThreshold - monthCycleMod) == 1:
    return True

  return False

# Flask Api Functions
@api.route('/vehicleStatus/query', methods=['POST'])
def post_vehicleStatus_query():
  '''Checks vehicle status against scrapping, distance maintainence and time maintainence conditions. Returns a json represnting the required notifications'''
  # validate input and throw error
  try:
    data = request.get_json()
  except:
    return badInputResponse

  if not validateJson(data):
    return badInputResponse

  # Setup check varibles
  purchaseDate = datetime.datetime.strptime(data["purchaseDate"], "%Y/%m/%d")
  submitDate = datetime.datetime.strptime(data["submitDate"], "%Y/%m/%d")
  isOverhauled = data["isOverhauled"]

  if checkShouldScrap(purchaseDate, submitDate, isOverhauled):
    return json.dumps(constructJson(isScrapped=True))

  if checkShouldDistanceMaintenance(data["odometer"]):
    return json.dumps(constructJson(isDistanceRelatedMaintenance=True))

  if checkShouldTimeMaintenance(purchaseDate, submitDate, isOverhauled):
    return json.dumps(constructJson(isTimeRelatedMaintenance=True))

  return json.dumps(constructJson())
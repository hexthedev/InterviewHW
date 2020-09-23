from flask import Flask, json, request, Response
import datetime

api = Flask(__name__)

badInputResponse = Response(status=418)

# dictionary expectedJsonInputKey : TypeValidationLambda
expectedKeys = {
  "submitDate" : lambda x : datetime.datetime.strptime(x, "%Y/%m/%d"),
  "purchaseDate" : lambda x : datetime.datetime.strptime(x, "%Y/%m/%d"),
  "odometer" : int,
  "isOverhauled": bool
}

def validateJson(json):
  if json is None:
    return False

  for k, v in expectedKeys.items():
    
    if k not in json:
      return False
    
    try:
      v(json[k])
    except ValueError:
      return False

  return True

@api.route('/vehicleStatus/query', methods=['POST'])
def post_vehicleStatus_query():
  
  # validate input and throw error
  try:
    data = request.get_json()
  except:
    # teapot error, because of bad input :)
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return badInputResponse

  if not validateJson(data):
    return badInputResponse

  # do we need to scrap
  return json.dumps(
    {
      "isTimeRelatedMaintenance": True,
      "isDistanceRelatedMaintenance": True,
      "isScrapped": True
    }
  )


  # do we need to distance maintain

  # do we need to time maintain
  



  #return json.dumps({"boop":"scoop"})


  # scrapped > distance > time



  # request
# {
#     // date of request submission, (used to determine condition)
#     "submitDate": "yyyy/MM/dd",

#     // date of purchase (used to determine condition)
#     "purchaseDate": "yyyy/MM/dd",

#     // for distance based condition. Assumed in km, not specified. 
#     "odometer": int,

#     // Has the vehicle been overhauled
#     "isOverhauled": bool
# }

# response
# {
#     // < 3 years, maintain every 12 months
#     // >= 3 years, maintain every 6 months
#     // if overhauled, maintain every 3 months
#     // remind one month in advance
#     isTimeRelatedMaintenance: bool
    
#     // every 10,000 km. Remind when next maintenance is <= 500 km.
#     isDistanceRelatedMaintenance: bool
    
#     // Non-overhauled: 2190 days after purchase
#     // Overhauled: 1095 days after purchase
#     // Remind one month in advance
#     isScrapped: bool
# }
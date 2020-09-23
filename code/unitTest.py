# run from command line, starts a development server used to test the api
# run as `python unitTest.py`, automatically attempts to create server at localhost:5000
#
# if for some reason then ip is in use, the following command can be run
# `python unitTest.py ip port` will use provided ip and port. 
# Will fail if ip or port are invalid 

import api.dadaApi as api
import sys
import requests

def requestWithoutJsonTest(url):
  res = requests.post(url = url)
  print(res)

def requestBadJsonTest(url):
  res = requests.post(url = url, json = {"bad" : "bad"})
  print(res)

def requestBadDateTest(url):
  res = requests.post(url = url, json = {
    "submitDate": "28/10/1992",
    "purchaseDate": "2010/10/28",
    "odometer": 10,
    "isOverhauled": True
  })
  print(res)

  res = requests.post(url = url, json = {
    "submitDate": "2010/10/28",
    "purchaseDate": "28/10/1992",
    "odometer": 10,
    "isOverhauled": True
  })
  print(res)

  res = requests.post(url = url, json = {
    "submitDate": "2010/10/28",
    "purchaseDate": "2010/10/28",
    "odometer": 10,
    "isOverhauled": True
  })
  print(res)


def runTests():
  args = sys.argv
  lenargs = len(args)

  # load the config json and detemrine host
  defaultServerIp = "localhost" 
  defaultServerPort = "5000" 

  serverIp = defaultServerIp if lenargs < 3 else args[1]
  serverPort = defaultServerPort if lenargs < 3 else args[2]

  url = f"http://{serverIp}:{serverPort}/vehicleStatus/query"
  
  requestWithoutJsonTest(url)
  requestBadJsonTest(url)
  requestBadDateTest(url)

if(__name__ == "__main__"):
  runTests()


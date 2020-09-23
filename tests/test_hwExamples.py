import requests
from helpers import constructAndSendRequest, checkJsonOutput, url

"""
Examples given as part of the homework assignment
"""

def test_example_1():
  res = constructAndSendRequest(url, "2030/09/01", "2025/04/05", 10000, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isDistanceRelatedMaintenance= True)

def test_example_2():
  res = constructAndSendRequest(url, "2030/09/01", "2029/10/14", 9000, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance = True)

def test_example_3():
  res = constructAndSendRequest(url, "2030/09/01", "2026/08/17", 13000, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json())

def test_example_4():
  res = constructAndSendRequest(url, "2030/09/01", "2027/11/01", 23000, True)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isScrapped= True)

def test_example_5():
  res = constructAndSendRequest(url, "2030/09/01", "2027/11/01", 19500, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isDistanceRelatedMaintenance= True)

def test_example_6():
  res = constructAndSendRequest(url, "2030/09/01", "2029/07/01", 10001, True)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isTimeRelatedMaintenance= True)

def test_example_7():
  res = constructAndSendRequest(url, "2030/09/01", "2028/04/19", 9800, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isDistanceRelatedMaintenance= True)

def test_example_8():
  res = constructAndSendRequest(url, "2030/09/01", "2027/07/10", 15000, True)
  assert res.status_code == 200
  assert checkJsonOutput(res.json())

def test_example_9():
  res = constructAndSendRequest(url, "2030/09/01", "2024/10/22", 90300, False)
  assert res.status_code == 200
  assert checkJsonOutput(res.json(), isScrapped=True)


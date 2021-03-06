"""
run from command line, starts a development server used to test the api
run as `python devServer.py`, automatically attempts to create server at localhost:5000

if for some reason then ip is in use, the following command can be run
`python devServer.py ip port` will use provided ip and port. 
Will fail if ip or port are invalid 
"""
import api.dadaApi as api
import sys

def initializeDevServer():
  # Determine the config path
  args = sys.argv
  lenargs = len(args)

  # load the config json and detemrine host
  defaultServerIp = "localhost" 
  defaultServerPort = "5000" 

  serverIp = defaultServerIp if lenargs < 3 else args[1]
  serverPort = defaultServerPort if lenargs < 3 else args[2]

  api.api.run(serverIp,serverPort)

if(__name__ == "__main__"):
    initializeDevServer()
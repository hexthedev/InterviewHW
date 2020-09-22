# simple script that runs the api as a local server
# console output will provide endpoint ip. Normall localhost:5000

import api.dadaApi as api

def run():
  api.api.run()

if(__name__ == "__main__"):
    run()
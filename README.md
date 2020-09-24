# InterviewHW

## Quick Start
This project contains a RESTApi endpoint implementation written using the Flask framework. To run the code locally, you will require:
* `Python 3.5+`
* The flask library `pip install Flask`
* The pytest library `pip install pytest`
* The requests library `pip install requests`

A development server can be run locally by running `python code/devServer.py <ip> <port>` from the project root. `python code/devServer.py` will create a server with default ip:port `localhost:5000`

To run unit tests:
1- Start a dev server on `localhost:5000`
2- Run `pytest -v` to run unit tests in verbose mode

The api implementation can be found at `code/api/dadaApi.py`

## Production
I did not implement a way to push this api to production. If this api needed pushing to some production endpoint, I would use a cloud based web application deplyoment service like `AWS Elastic Beanstalk`.

Each service has it's own requirements when it comes to deployment. But the mostly likely scenario would be to push the code in `code/api` to the deplyoment server using AWS Cli commands. 

This would allow for CI/CD integration whenever changes were pushed to the `master` branch. It's could be automated through GitHub Actions, or another DevOps alternative. 

## Notes and Future Improvements
* I don't like that the dev server needs starting to run unit tests. I would rather run unit tests automatically start and stop the application per test, as a test fixture. In this case, since the application is stateless, it isn't a problem though. 

* I don't like that unit tests are locked to an ip. I would try to find a solution to this using a configuration json file used by unit test requests and the tested application. 

## Problem interpretation
Need to create a simple RESTApi, that has a single POST request used to determine the whether maintenance is required. 

The format of the request/ response is as follows:

```
# request
{
    // date of request submission, (used to determine condition)
    "submitDate": "yyyy/MM/dd",

    // date of purchase (used to determine condition)
    "purchaseDate": "yyyy/MM/dd",

    // for distance based condition. Assumed in km, not specified. 
    "odometer": int,

    // Has the vehicle been overhauled
    "isOverhauled": bool
}

# response
{
    // < 3 years, maintain every 12 months
    // >= 3 years, maintain every 6 months
    // if overhauled, maintain every 3 months
    // remind one month in advance
    isTimeRelatedMaintenance: bool
    
    // every 10,000 km. Remind when next maintenance is <= 500 km.
    isDistanceRelatedMaintenance: bool
    
    // Non-overhauled: 2190 days after purchase
    // Overhauled: 1095 days after purchase
    // Remind one month in advance
    isScrapped: bool
}
```

## Special Notes:
* If a vehicle is reminded to be scrapped, no maintenance is required. 
* In the case where both time and distance maintenance are required, distance takes priority.  

## Things I noticed
* There is no mention of id, and api response can always be calculted from request. Therefore, now database is required. 

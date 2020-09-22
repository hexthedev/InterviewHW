# InterviewHW
This repo contains my code homework. I'll delete the repo once complete so that others can't find an answer. I'm also refraining from using the actual name of who I'm interviewing for, as not to ruin the interview process (by giving others a copy paste answer).


# Problem interpretation
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
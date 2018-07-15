# Interview Code Submission

## Requirements
- Python 2
- Python pip
- requests
    - `pip install requests`
- Beautifulsoup4
    - `pip install beautifulsoup4`

You can also install the requirements from the requirements.txt file

```
pip install -r requirements.txt
```

## Running
```
python tides.py > out.json
```

The script produces the low tide data in a json format. I did this because it generally is nicer 
to have things in a structured format instead of an ad-hoc one. The format of the json output is:

```
{
    "location-name1": [ # list of low tides
        {
            "date": (str) date of the low tide,
            "time": (str) time of the low tide,
            "time_zone": (str) time zone,
            "level_metric": (str) low tide level in metric, 
            "level_std": (str) low tide level in standard, 
            "event": (str) event name -- should always be "Low Tide"
        }
    ],
 
    "location-name2: [ 
 	... 
    ], 
    ...
}
``` 

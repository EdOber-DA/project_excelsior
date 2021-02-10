from config import alphavantage_key as api_key
import pandas as pd
import requests
from pprint import pprint
import json
#This bring in the hourly trade data
for i in range(1,6):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=GME&interval=60min&slice=year1month{i}&apikey={api_key}'
    #this returns a CSV
    res = requests.get(url)
    open(f'../Data/{i}_months_before_.csv', 'wb').write(res.content)
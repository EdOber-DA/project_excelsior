import praw
from datetime import datetime
import pandas as pd
import requests
import time
comment_counts = {}
current_time = 1611759600
#9/1/20202 00:00:00 1598932800
while(current_time > 1611464400):
    url = f'https://api.pushshift.io/reddit/comment/search/?after={current_time-720}&before={current_time}&subreddit=wallstreetbets&q=gme&size=100&score=%3E5'
    res = requests.get(url).json()
    try:
        date = datetime.fromtimestamp(res['data'][0]['created_utc']).strftime('%m/%d/%Y %H:00')
        time.sleep(0.3)
    except:
        print(res)
        current_time -= 720
        continue
    if date in comment_counts:
        comment_counts[date] += len(res['data'])
    else:
        comment_counts[date] = len(res['data'])
    current_time -= 720


dates = []
comments = []
for k,v in comment_counts.items():
    dates.append(k)
    comments.append(v) 
#Create a dataframe from the data taken from reddit 
df = pd.DataFrame({'Date': dates, '# of Comments': comments})
df.to_csv('Data/Raw Data/specific_data.csv')


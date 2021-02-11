import praw
from config import client_id, secret
from datetime import datetime
import pandas as pd

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent="ckioski"
)
subreddit = reddit.subreddit('wallstreetbets')
comment_counts = {}
for submission in subreddit.search(query='GME',sort='comments',time_filter='year',limit=None):
    print(1)
    #unix time for Feb 3rd as 12:00 am.  We are only looking at posts from before that 
    if submission.created_utc > 1612328400:
        continue
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        try:
            print(comment.created_utc)
            if 'GME' in comment.body:
                date = datetime.fromtimestamp(comment.created_utc).strftime('%m/%d/%Y %H:00')
                if date in comment_counts:
                    comment_counts[date] += 1
                else:
                    comment_counts[date] = 1
        except:
            pass
dates = []
comments = []
for k,v in comment_counts.items():
    dates.append(k)
    comments.append(v) 
#Create a dataframe from the data taken from reddit 
df = pd.DataFrame({'Date': dates, '# of Comments': comments})
df.to_csv('Data/comment_results.csv')



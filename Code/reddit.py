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
count = 0
comment_bodies = []
for submission in subreddit.search(query='GME',sort='comments',time_filter='year',limit=None):
    if submission.created_utc > 1612328400:
        continue
    top_level_comments = list(submission.comments)
    for comment in top_level_comments:
        #we are only looking at top level comments, so no comments of comments
        if type(comment) != praw.models.MoreComments:
            if 'GME' in comment.body:
                count += 1
    #takes unix timestamp and converts to datetime object so it is readable
    date = datetime.fromtimestamp(submission.created_utc).strftime('%m/%d/%Y')
    if date in comment_counts:
        comment_counts[date] += count
    else:
        comment_counts[date] = count
    count = 0
    comment_bodies = []

#Running the same test on r/WallStreetBetsNew
subreddit = reddit.subreddit('wallstreetbetsnew')
for submission in subreddit.search(query='GME',sort='comments',time_filter='year',limit=None):
    if submission.created_utc > 1612328400:
        continue
    top_level_comments = list(submission.comments)
    for comment in top_level_comments:
        #we are only looking at top level comments, so no comments of comments
        if type(comment) != praw.models.MoreComments:
            if 'GME' in comment.body:
                count += 1
    #takes unix timestamp and converts to datetime object so it is readable
    date = datetime.fromtimestamp(submission.created_utc).strftime('%m/%d/%Y')
    if date in comment_counts:
        comment_counts[date] += count
    else:
        comment_counts[date] = count
    count = 0
    comment_bodies = []

dates = []
comments = []
for k,v in comment_counts.items():
    dates.append(k)
    comments.append(v) 

df = pd.DataFrame({'Date': dates, '# of Comments': comments})
df.to_csv('results.csv')



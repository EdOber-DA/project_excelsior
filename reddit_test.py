import praw
from config import client_id, secret
from datetime import datetime


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent="ckioski"
)
subreddit = reddit.subreddit('wallstreetbets')
#this is 2/4/2021 at 12:00 am, anything 48 hours before is 2/2/2021 which is our final search date
#2/4/2021 at 12:00 am ->  1612396800
#needs to be current/when full looking is workign for 1000 at a time, can be our set date
time_break = 1612656000
one_day = 86400
comment_counts = {}
count = 0
prev_sub_utc = 0

for submission in subreddit.search(query='walmart',sort='new',time_filter='year',limit=None):
    if submission.created_utc <= (time_break - one_day):
        #takes unix timestamp and converts to datetime object 
        date = datetime.fromtimestamp(prev_sub_utc).strftime('%m/%d/%Y')
        if date in comment_counts:
            comment_counts[date] += count
        else:
            comment_counts[date] = count
        count = 0
        time_break = time_break - one_day
    for comment in submission.comments:
        while True:
            try:
                if 'gme' in comment.body.lower():
                    count = count + 1
                break
            #if MultiComment error, run this block 
            except AttributeError:
                comment = comment.comments()
                for c in comment:
                    try:
                        if 'gme' in c.body.lower():
                            count = count + 1
                    
                    #if there is a multicomment inside a multicomment, we will ignore it 
                    except AttributeError:
                        pass
                break
    prev_sub_utc = submission.created_utc

#make sure i append the day for 2/1/2020
comment_counts[(datetime.fromtimestamp(prev_sub_utc)).strftime('%m/%d/%Y')] = count
#reversing so it goes in order from 2/1/2020 to 2/2/2021
print(comment_counts)
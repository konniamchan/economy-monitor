#! /usr/bin/python

'''Count tweets from last hour (for totals and keywords). cleans up 
last_hour_tweets database.'''

import psycopg2 as pg
import pymongo as pm
import datetime as dt
import re

# Keyword terms
kwd_terms = [r'lost +(my|his|her|your|their)? *job',
             r'got *fired',r'unemploy(ed)?',r'lay(ed )?-?off']

# Postgres connection
conn    = pg.connect(user='w205',database='w205project',password='pw')
cur     = conn.cursor()

# Mongo connection
client      = pm.MongoClient()
db          = client["w205"]
tweets_db   = db["twitter"]
deleted_db  = db["deleted"]

#get datetime info
now = dt.datetime.now()
nowHour = now.replace(minute=0,second=0,microsecond=0)
hourAgo = now - dt.timedelta(hours=1)

#setup tallys
total_count = 0
kwd_counts = dict.fromkeys(kwd_terms,0)

#get tweet ids for last hour (from postgres table last_hour_tweets)
cur.execute("SELECT tweet_id FROM last_hour_tweets WHERE timestamp>=%s AND timestamp<%s", (hourAgo.isoformat(), now.isoformat()) )
tweets = cur.fetchall()
conn.commit()

#iterate over tweet ids ('_id')
for twt in tweets:
    #get tweets from mongodb and search for keyword terms
    for k in kwd_terms:
        tweet   = tweets_db.find_one({'_id':twt[0]})
        text    = tweet['text'].lower()
        if re.search(k, text):
            #tally results
            kwd_counts[k] += 1
    total_count += 1            

#update total_tweets postgres table
cur.execute("INSERT INTO total_tweets VALUES (%s, %s)", (nowHour.isoformat(), total_count))
conn.commit()

#update keyword_tweets_cnt postgres table
for key,val in kwd_counts.items():
    cur.execute("INSERT INTO keyword_tweets_cnt VALUES (%s, %s, %s)", (nowHour.isoformat(), key, val))
                                                                 
#drop old data
cur.execute("DELETE FROM last_hour_tweets WHERE timestamp<%s", (now.isoformat(), ))
conn.commit()

cur.close()
conn.close()

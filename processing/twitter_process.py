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
nowHour = dt.datetime.now().replace(minute=0,second=0,microsecond=0)
hourAgo = nowHour - dt.timedelta(hours=1)

#setup tallys
total_count = 0
kwd_counts = dict.fromkeys(kwd_terms,0)

#get tweet ids for last hour (from postgres table last_hour_tweets)
cmd     = "SELECT tweet_id FROM last_hour_tweets WHERE " +\
          "timestamp>='%s' AND timestamp<'%s'" %(hourAgo.isoformat(),
                                                 nowHour.isoformat()
                                                 )
cur.execute(cmd)

#iterate over tweet ids ('_id')
for twt in cur:
    #get tweets from mongodb and search for keyword terms
    for k in kwd_terms:
        tweet   = tweets_db.find_one({'_id':twt[0]})
        text    = tweet['text']
        if re.search(k,text):
            #tally results
            kwd_counts[k] += 1
    total_count += 1            

#update total_tweets postgres table
cmd = "INSERT INTO total_tweets VALUES ('%s','%d')" %(nowHour.isoformat(),
                                                      total_count
                                                      )
cur.execute(cmd)

#update keyword_tweets_cnt postgres table
for key,val in kwd_counts.items():
    cmd = "INSERT INTO keyword_tweets_cnt VALUES " +\
          "('%s','%s','%d')" %(nowHour.isoformat(), key, val)
    cur.execute(cmd)
                                                                 
#drop old data
cmd = "DELETE FROM last_hour_tweets WHERE timestamp<'%s'" %(hourAgo.isoformat())
cur.execute(cmd)


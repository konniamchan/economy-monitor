# Batch process tweets in MongoDB to pull out counts of keywords
import psycopg2 as pg
import pymongo as pm
import datetime as dt
import re

# Keyword terms
kwd_terms = [r'lost +(my|his|her|your|their)? *job',
             r'got *fired',r'unemploy(ed)?',r'la(y|id)?[ -]?off']

# Postgres connection
conn    = pg.connect(user='w205',database='w205project',password='pw')
cur     = conn.cursor()

# Mongo connection
client      = pm.MongoClient()
db          = client["w205"]
tweets_db   = db["twitter"]

# Initialize PostgreSQL table
start_time = dt.datetime(2015, 12, 1, 0)
end_time = dt.datetime(2015, 12, 15, 0)
time = start_time

while time <= end_time:
    # Total count
    cur.execute("INSERT INTO total_tweets VALUES (%s, %s)", (time.isoformat(), 0))
    conn.commit()
    # Keyword count
    for k in kwd_terms:
        cur.execute("INSERT INTO keyword_tweets_cnt VALUES (%s, %s, %s)", (time.isoformat(), k, 0))
        conn.commit()
    time = time + dt.timedelta(hours=1)
    
# Iterate through tweets to record counts
for tweet in tweets_db.find():
    # Parse and group into hour
    created_time = dt.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
    created_time = created_time.replace(minute=0,second=0,microsecond=0)

    # Get and update total count
    cur.execute("SELECT count FROM total_tweets WHERE timestamp = %s", (created_time.isoformat(), ))
    total_count = cur.fetchone()
    conn.commit()    
    cur.execute("UPDATE total_tweets SET count=%s WHERE timestamp = %s", (total_count[0]+1, created_time))
    conn.commit()

    # Check if tweet contains keyword
    for k in kwd_terms:
        if re.search(k, tweet['text'].lower()):
            # Get and update keyword count
            cur.execute("SELECT count FROM keyword_tweets_cnt WHERE timestamp = %s AND kword_search = %s", (created_time.isoformat(), k))
            keyword_count = cur.fetchone()
            conn.commit()            
            cur.execute("UPDATE keyword_tweets_cnt SET count=%s WHERE timestamp = %s AND kword_search = %s", (keyword_count[0]+1, created_time, k))
            conn.commit()

cur.close()
conn.close()

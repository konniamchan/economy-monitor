from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import simplejson
import psycopg2 as pg
import datetime as dt

# Kafka consumer
consumer = KafkaConsumer('twitter', group_id='twitter-group', bootstrap_servers=['localhost:9092'])

# Mongo connection
client = MongoClient()
db = client["w205"]
tweets_db = db["twitter"]
deleted_db = db["deleted"]
print ("Started writing to Mongo...")

# Postgres connection
conn    = pg.connect(user='w205',database='w205project',password='pw')
cur     = conn.cursor()

# Collection
for message in consumer:
    # message value is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    tweet = simplejson.loads(message.value)
    if 'delete' in tweet:
        tweet['_id'] = tweet['delete']['status']['id_str']
        del tweet['delete']['status']['id_str']
        try:
            deleted_db.insert_one(tweet)
        # Catch duplicate delete messages
        except DuplicateKeyError:
            pass
    
    elif 'lang' in tweet:
        if tweet['lang'] == 'en':
            tweet['_id'] = tweet['id_str']
            del tweet['id_str']
            # Catch duplicate tweets
            try:
                #insert tweet id to postgres last_hour_tweets table
                dtime   = dt.datetime.isoformat(dt.datetime.now())
                cmd     = 'INSERT INTO last_hour_tweets VALUES ' +\
                          "('%s','%s')" %(dtime,tweet['_id'])
                cur.execute(cmd)                
                #insert data to mongo tweets_db database
                tweets_db.insert_one(tweet)            
            except DuplicateKeyError:
                pass
    else:
        pass

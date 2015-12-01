from kafka import KafkaConsumer
from pymongo import MongoClient
import simplejson

# Kafka consumer
consumer = KafkaConsumer('twitter', group_id='twitter-group', bootstrap_servers=['localhost:9092'])

# Mongo connection
client = MongoClient()
db = client["w205"]
tweets_db = db["twitter"]
deleted_db = db["deleted"]

# Collection
for message in consumer:
    # message value is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    tweet = simplejson.load(message.value)
    if 'delete' in tweet:
        tweet['_id'] = tweet['delete']['status']['id_str']
        del tweet['delete']['status']['id_str']
        deleted_db.insert_one(tweet)
    
    elif 'lang' in tweet:
        if tweet['lang'] == 'en':
            tweet['_id'] = tweet['id_str']
            del tweet['id_str']
            tweets_db.insert_one(tweet)
    else:
        pass

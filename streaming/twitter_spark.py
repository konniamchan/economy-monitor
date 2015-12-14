# Spark Streaming Component
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import simplejson
import re

# Spark and streaming contexts
sc = SparkContext("local[2]", "twitter")
ssc = StreamingContext(sc, 10)
kafka_stream = KafkaUtils.createStream(ssc, "localhost:2181", "twitter-consumer", {"twitter":1} )

# Ceate RDD's
tweets_parsed = kafka_stream.map(lambda (n,x): simplejson.loads(x))
tweets_filtered = tweets_parsed.filter (lambda x: 'text' in x)
tweets = tweets_filtered.map(lambda x: x['text'].encode('utf-8').lower())

# Count keyword frequencies
# kwd_terms = [r'lost +(my|his|her|your|their)? *job',
#              r'got *fired',r'unemploy(ed)?',r'lay(ed )?-?off']
kwd_terms = ["iphone", "ipad", "samsung", "android"]
kwd_rdd = [None, None, None, None]


kwd_rdd[0] = tweets.filter(lambda x: re.search(kwd_terms[0], x))
kwd_rdd[0].pprint()
kwd_rdd[0].count().pprint()

kwd_rdd[1] = tweets.filter(lambda x: re.search(kwd_terms[1], x))
kwd_rdd[1].pprint()
kwd_rdd[1].count().pprint()

kwd_rdd[2] = tweets.filter(lambda x: re.search(kwd_terms[2], x))
kwd_rdd[2].pprint()
kwd_rdd[2].count().pprint()

kwd_rdd[3] = tweets.filter(lambda x: re.search(kwd_terms[3], x))
kwd_rdd[3].pprint()
kwd_rdd[3].count().pprint()

tweets.count().pprint()

ssc.start()
ssc.awaitTermination()
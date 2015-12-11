from __future__ import absolute_import, print_function
from kafka import SimpleProducer, KafkaClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_credentials import *

# Kafka: send messages synchronously
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)

# Twitter streaming -> Kafka
class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    Send stream to Kafka.
    """
    def on_data(self, raw_data):
        try:
            producer.send_messages(b'twitter', raw_data.strip().encode('utf-8'))
            return(True)
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print ("Starting ingestion...")   

    stream = Stream(auth, l)
    stream.sample()





from textblob import TextBlob
from elasticsearch import Elasticsearch
import uuid
import json
from datetime import datetime

# Elastic Connection
es = Elasticsearch(hosts="localhost")
index_name = 'trump-' + datetime.now().strftime('%Y.%m.%d')

def check_elastic():
    if not es.indices.exists('trump'):
        mapping = """
        {
        "settings": {
            "index.number_of_shards": 1,
            "index.number_of_replicas": 0
        }
        }
        """
        es.indices.create(index=index_name, body=mapping)

   

# Data Model
class Tweet(object):
    def __init__(self, username, realname, location, tweet_text, hashtags):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.username = username
        self.realname = realname
        self.location = location
        self.tweet_text = tweet_text
        self.hashtags = [hash["text"] for hash in hashtags]
        self.sentiment = self.get_sentiment()

    def get_sentiment(self):
        return TextBlob(self.tweet_text).sentiment.polarity

    def push_to_elastic(self):
        es.index(
            index=index_name,
            doc_type="tweets",
            id=self.id,
            body={
                    "@timestamp": self.timestamp,
                    "user": self.username,
                    "realname": self.realname,
                    "location": self.location,
                    "tweet": self.tweet_text,
                    "hashtags": self.hashtags,
                    "sentiment": self.sentiment,
                }
        )
    
    def get_details(self):
        print(self.timestamp, self.username, self.tweet_text, self.hashtags, self.sentiment)


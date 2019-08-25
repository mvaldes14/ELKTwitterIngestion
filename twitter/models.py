from textblob import TextBlob
from elasticsearch import Elasticsearch
import uuid
import json
from datetime import datetime
import re

# Elastic Connection
es = Elasticsearch(hosts="localhost", http_auth=("elastic", "elastic"))
index_name = "trump-" + datetime.now().strftime("%Y.%m.%d")


# Data Model
class TweetStream(object):
    def __init__(
        self, username, realname, location, tweet_text, hashtags, reply, trump_tweet
    ):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.username = username
        self.realname = realname
        self.location = location if location else None
        self.tweet_text = self.clean_tweet(tweet_text)
        self.hashtags = [hash["text"] for hash in hashtags]
        self.sentiment = self.get_sentiment()
        self.reply = reply
        self.trump_tweet = trump_tweet

    def clean_tweet(self, tweet_text):
        pattern = re.compile("((RT\s)?[@][\w_-]+)")
        return re.sub(pattern, "", tweet_text).lstrip()

    def get_sentiment(self):
        return TextBlob(self.tweet_text).sentiment.polarity

    def push_to_elastic(self):
        es.index(
            index=index_name,
            doc_type="_doc",
            id=self.id,
            body={
                "@timestamp": self.timestamp,
                "user": self.username,
                "realname": self.realname,
                "location": self.location,
                "tweet": self.tweet_text,
                "hashtags": self.hashtags,
                "sentiment": self.sentiment,
                "reply": self.reply,
                "trump_tweet": self.trump_tweet,
            },
        )

    def __repr__(self):
        return self.username + " " + self.tweet_text

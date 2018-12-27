from textblob import TextBlob
from elasticsearch import Elasticsearch


class Tweet(object):
    def __init__(self, username, tweet_text, hashtags):
        self.username = username
        self.tweet_text = tweet_text
        self.hashtags = [hash for hash in hashtags if hash]
        self.sentiment = self.get_sentiment()

    def get_sentiment(self):
        return TextBlob(self.tweet_text).sentiment.polarity

    def get_details(self):
        return (self.username, self.tweet_text, self.hashtags, self.sentiment)

#es = Elasticsearch(hosts='localhost')
#print(es.cat.health())
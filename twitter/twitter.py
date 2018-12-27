from twython import Twython
from twython import TwythonStreamer
from models import Tweet

CONSUMER_KEY = "V1XCyXScnXDZh232FAIvjSd2e"
CONSUMER_SECRET = "JOB36LqZhd8A6WJ4zmd7ZBy3As2CQhK9uLXonlpaliFJYMhcSv"
AUTH_TOKEN = "43233942-pMGIuekO53ZywjjOe3JVZJoekOLWN5KzIfj1NcvKP"
AUTH_SECRET = "ibXRDGgO4g9WA8buMFvzfyJebA6JkhCN26WMUeGeA"


# twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, AUTH_TOKEN, AUTH_SECRET)
# tweets = twitter.search(q="Trump", count=1, tweet_mode="extended")
# for i in tweets["statuses"]:
#     print(i)
#     tweet1 = Tweet(
#         username=i["user"]["screen_name"],
#         tweet_text=i["full_text"],
#         hashtags=i["entities"]["hashtags"],
#     )
#     print(tweet1.get_details())

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
            print(data)

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()
        return False

    def on_timeout(self, data):
        print("Request timed out, try again later")
        self.disconnect()

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, AUTH_TOKEN, AUTH_SECRET)
stream.statuses.filter(track='python')



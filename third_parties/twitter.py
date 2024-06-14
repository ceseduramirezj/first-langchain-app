import tweepy
import os
import requests

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
)

def scrape_user_tweets(username, num_tweets=5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets) and return them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text" and "url".
    """

    if mock:
        EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
        tweets: list[dict] = requests.get(EDEN_TWITTER_GIST, timeout= 5).json()

    else:
        user_id = twitter_client.get_user(username= username).data.id
        tweets: list[dict] = twitter_client.get_users_tweets(
            id= user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        ).data

    tweet_list: list[dict] = list(map(lambda tweet: {
        "text": tweet["text"],
        "url": f"https://twitter.com/{username}/status/{tweet['id']}"
    }, tweets))
    
    return tweet_list

if __name__ == "__main__":
    tweets = scrape_user_tweets(username="EdenEmarco177", mock= True)
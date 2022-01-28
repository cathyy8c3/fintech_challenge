import os
import tweepy as tw
import pandas as pd
from textblob import TextBlob
import requests
import json
import time
import psycopg2
from datetime import datetime
import time

APP_KEY = 'GqqEIjRQAWAdFztL4mnMEBaVo'
APP_SECRET = 'CHhUU0AA637K3geo9DllzZrCQUqOKi3fJJU4KCxiZr4cWCZxrp'
ACCESS_TOKEN = '1484263593705041921-e0sChgdl3Q0IeJIT5hXhpFP8cx4eb'
ACCESS_TOKEN_SECRET = 'UK6rMKnYjbbUnvZF12K2RWDqjks1GTVBeC5hSuDnnaoRc'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIlXYQEAAAAAKVq4cfWjJUd%2BaAJN7HzW5%2FiKN3M%3DFfUbWj2WgNFVWaSHOkUcyIJHaddppNFqrEjXhlQ0zLcAYl2Cre'

def timestamp_to_utc(timestamp):
    TIME_FORMAT='%Y-%m-%d %H:%M:%S'
    d = datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
    return d

# 500,000 max queries per month
# can only get tweets from last week
# max_results = number of tweets to get (max val 100)
def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN, max_results = 0):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    # change max_results to query more tweets, max 100
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields, max_results = max_results
    )
    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# keyword = word we are searching for
# since_date = date of oldest comment or post
# num = number of results in response
def search_reddit(keyword, since_date, num = 500):
    url = "https://api.pushshift.io/reddit"

    query_posts = {'title': keyword, 'after': since_date, 'size': num, 'score': '>10'}
    query_comments = {'q': keyword, 'after': since_date, 'size': num}

    posts = requests.get(url + "/search/submission/?q:not=bot" + "&title=" + keyword + "&size=500" + "&subreddit=wallstreetbets,CryptoCurrency" + "&after=" + since_date + "&score=>0")
    comments = requests.get(url + "/search/comment/?q=" + keyword + "&size=500" + "&subreddit=wallstreetbets,CryptoCurrency" + "&after=" + since_date)

    if posts.status_code != 200:
        raise Exception(posts.status_code, posts.text)
    if comments.status_code != 200:
        raise Exception(comments.status_code, comments.text)

    return posts.json(), comments.json()

# adds tweets / posts / comments with timestamps to dataframe
# query = keyword that is searched for
# since_date only applies to reddit
# default since_date is set to a week back
# since_date = int + "s,m,h, or d" (ex: '7d' = returns tweets after 7 days ago)
def sentiment_analysis(query, df_twitter, df_reddit, since_date = '7d'):
    tweet_fields = "tweet.fields=text,created_at"
    twitter = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN, max_results=100)
    #twitter = {'data': []}
    reddit_posts, reddit_comments = search_reddit(query, since_date)

    twitter_timestamps = []
    tweets = []
    for tweet in twitter['data']:
        try:
            tweet['text']
        except:
            continue
        tweets.append(tweet['text'])
        twitter_timestamps.append(tweet['created_at'])

    for i in range(len(tweets)):
        blob = TextBlob(tweets[i])
        sentiment = blob.sentiment.polarity

        df_twitter.loc[tweets[i]] = {'Ticker': query, 'Timestamp': twitter_timestamps[i], 'Sentiment': sentiment}

    reddit_timestamps_posts = []
    r_posts = []
    for post in reddit_posts['data']:
        try:
            post['selftext']
        except:
            continue
        r_posts.append(post['selftext'])   # only analyzing sentiment of title
        reddit_timestamps_posts.append(timestamp_to_utc(post['created_utc']))

    for i in range(len(r_posts)):
        blob = TextBlob(r_posts[i])
        sentiment = blob.sentiment.polarity

        df_reddit.loc[r_posts[i]] = {'Ticker': query, 'Timestamp': reddit_timestamps_posts[i], 'Sentiment': sentiment}

    reddit_timestamps_comments = []
    r_comments = []
    for comment in reddit_comments['data']:
        try:
            comment['body']
        except:
            continue
        r_comments.append(comment['body'])
        reddit_timestamps_comments.append(timestamp_to_utc(comment['created_utc']))

    for i in range(len(r_comments)):
        blob = TextBlob(r_comments[i])
        sentiment = blob.sentiment.polarity

        df_reddit.loc[r_comments[i]] = {'Ticker': query, 'Timestamp': reddit_timestamps_comments[i], 'Sentiment': sentiment}

    # sentiment ranges from [-1, 1], where -1 is negative sentiment and 1 is positive sentiment
    # sum_twitter = 0
    # for tweet in tweets:
    #     blob = TextBlob(tweet)
    #     sentiment = blob.sentiment.polarity
    #     sum_twitter += sentiment
    # try:
    #     avg_twitter_sentiment = float(sum_twitter) / len(tweets)
    # except:
    #     avg_twitter_sentiment = 0
    #
    # sum_reddit = 0
    # for post in r_posts:
    #     blob = TextBlob(post)
    #     sentiment = blob.sentiment.polarity
    #     sum_reddit += sentiment
    # for comment in r_comments:
    #     blob = TextBlob(comment)
    #     sentiment = blob.sentiment.polarity
    #     sum_reddit += sentiment
    #
    # try:
    #     avg_reddit_sentiment = float(sum_reddit) / (len(r_posts) + len(r_comments))
    # except:
    #     avg_reddit_sentiment = 0
    #
    # return avg_twitter_sentiment, avg_reddit_sentiment, tweets, r_posts, r_comments, twitter_timestamps, reddit_timestamps_posts, reddit_timestamps_comments

# adds crypto data to dataframe with average sentiment
# query = keywords searched for
# since_date only applies to reddit
# since_date = int + "s,m,h, or d" (ex: '7d' = returns tweets after 7 days ago)
def add_crypto(df_twitter, df_reddit, query, since_date = '7d'):
    avg_twitter_sentiment, avg_reddit_sentiment, tweets, r_posts, r_comments, twitter_timestamps, reddit_timestamps_posts, reddit_timestamps_comments = sentiment_analysis(query, since_date = since_date)

    # list of each tweet with timestamp
    tweets_timestamps = []
    for i in range(len(tweets)):
        tweets_timestamps.append([tweets[i], twitter_timestamps[i]])

    # list of each reddit post with timestamp
    r_posts_timestamps = []
    for i in range(len(r_posts)):
        r_posts_timestamps.append([r_posts[i], reddit_timestamps_posts[i]])

    # list of each reddit comment with timestamp
    r_comments_timestamps = []
    for i in range(len(r_comments)):
        r_comments_timestamps.append([r_comments[i], reddit_timestamps_comments[i]])

    reddit_combined = r_posts_timestamps + r_comments_timestamps

    df_twitter.loc[query] = pd.Series({'Average Sentiment': avg_twitter_sentiment, 'Tweet': tweets_timestamps})
    df_reddit.loc[query + '_' + since_date] = pd.Series({'Average Sentiment': avg_reddit_sentiment, 'Posts / Comments': reddit_combined})

conn = psycopg2.connect(
    database="tsdb",
    user="tsdbadmin",
    password="s076ypajb1f2sx6z",
    host="sjlvg6tey5.y7ed71zc7s.tsdb.cloud.timescale.com",
    port="39863"
)

conn.autocommit = True
cursor = conn.cursor()

df_twitter = pd.DataFrame(columns = ['Ticker', 'Timestamp', 'Sentiment'])
df_reddit = pd.DataFrame(columns = ['Ticker', 'Timestamp', 'Sentiment'])

crypts = ['BTC', 'ETH', 'BNB', 'USDT', 'SOL', 'USDC', 'ADA', 'XRP', 'LUNA', 'DOT', 'AVAX', 'DOGE']

df_twitter.sort_values('Timestamp')
df_reddit.sort_values('Timestamp')

def post_to_db(crypt, df_twitter, df_reddit):
    sentiment_analysis(crypt, df_twitter, df_reddit, '24h')
    sentiment_analysis(crypt, df_twitter, df_reddit, '7d')
    sentiment_analysis(crypt, df_twitter, df_reddit, '365d')

    for index, row in df_twitter.iterrows():
        source = 'T'
        ticker = row['Ticker']
        text = index
        timestamp = row['Timestamp']
        sentiment = row['Sentiment']

        print(timestamp, ticker, text, sentiment, source)
        try:
            cursor.execute('''SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE''')
            cursor.execute('''INSERT INTO sentiments(timestamp, ticker, text, sentiment, source) VALUES(%s, %s, %s, %s, %s)''', (str(timestamp), str(ticker), str(text), sentiment, str(source),))
        except:
            continue

    for index, row in df_reddit.iterrows():
        source = 'R'
        ticker = row['Ticker']
        text = index
        timestamp = row['Timestamp']
        sentiment = row['Sentiment']

        print(timestamp, ticker, text, sentiment, source)

        try:
            cursor.execute('''SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE''')
            cursor.execute('''INSERT INTO sentiments(timestamp, ticker, text, sentiment, source) VALUES(%s, %s, %s, %s, %s)''', (str(timestamp), str(ticker), str(text), sentiment, str(source),))
        except:
            continue

for crypt in crypts:
    post_to_db(crypt, df_twitter, df_reddit)

conn.commit()
print("Pushed To Dataframe...")
conn.close()

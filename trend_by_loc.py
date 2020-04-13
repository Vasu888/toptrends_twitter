
#Collects top trends in a location by WOECID
#Plot graphs with tweet volumes for these trends
#for each of the top 10 tweets of each trend, like the tweet and follow the user

# -*- coding: utf-8 -*-
import sys
import os
import tweepy
import json
import operator
from operator import itemgetter
from googletrans import Translator
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.font_manager._rebuild()
#For Japanese font
matplotlib.rc('font', family='Noto Sans CJK JP')

#API Keys - Replace xxx with your app keys
consumer_key = 'xxx'
consumer_secret = 'xxx'
access_token = 'xxx'
access_token_secret = 'xxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Where On Earth ID for Brazil is 23424768.
jp_id = 23424856
tokyo_id = 1118370
woe_id = jp_id
translator = Translator()

#cleanup old files
os.system("rm -rf data")
os.system("mkdir data")

raw_trends_by_loc = api.trends_place(tokyo_id, '#')
#print (raw_trends_by_loc)
trends = raw_trends_by_loc[0]["trends"]

# Remove trends with no Tweet volume data
trends = filter(itemgetter("tweet_volume"), trends)

#sort trends by tweet volume data
sorted_trends = sorted(trends, key=itemgetter("tweet_volume"), reverse=True)
df = pd.DataFrame(sorted_trends)
print (df)
df.to_csv("trends_by_loc.csv", encoding="utf-8")

plt_type = ['line', 'bar', 'barh', 'hist',  'area']

for graph_type in plt_type:
    df.plot(kind=graph_type,x='name',y='tweet_volume')
    filename = graph_type+".png"
    plt.savefig(filename)

os.system("mv *.png data/")
os.system("mv *.csv data/")

i = 1
j = 1
errors = 0

#Getting the top 10 tweets for each trend
for trend_values in df.loc[:, "name"]:
    print (trend_values)
    tweets_of_trend = tweepy.Cursor(api.search, q=trend_values, tweet_mode='extended').items(10)
    for tweets in tweets_of_trend:
        try:
            api.create_favorite(tweets.id)
            tweets.user.follow()
        except tweepy.TweepError:
            errors += 1
        except StopIteration:
            continue                  


# Chapter 1 Mining the Social Web 2nd Ed
#############################################################
# 1.3.3 Exploring Trending Topics
#############################################################
 
import twitter
from credentials import *

auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

twitter_api = twitter.Twitter(auth=auth)
# print twitter_api

# The Yahoo! Where On Earth ID for the entire world is 1.
# See https://dev.twitter.com/docs/api/1.1/get/trends/place and
# http://developer.yahoo.com/geo/geoplanet/

WORLD_WOE_ID = 1
US_WOE_ID = 23424977

# Prefix ID with the underscore for query string parameterization.
# Without the underscore, the twitter package appends the ID value
# to the URL itself as a special case keyword argument.

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)
# print world_trends
# print
# print us_trends

import json
# print json.dumps(world_trends, indent=1)
# print json.dumps(us_trends, indent=1)

world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
us_trends_set = set([trend['name'] for trend in us_trends[0]['trends']])
common_trends = world_trends_set.intersection(us_trends_set)
print common_trends
print world_trends_set
print us_trends_set

#############################################################
# 1.3.4 Searching for Tweets
#############################################################
from urllib import unquote
q = '#TheNewsIn4Words'
count = 100
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']


# Iterate through 5 more batches of results by following the cursor
for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist
        break

    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=%23TheNewsIn4Words&include_entities=1
    kwargs = dict([kv.split('=') for kv in unquote(next_results[1:]).split("&") ])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']
    
# Show one sample search result by slicing the list...
print json.dumps(statuses[0], indent=1)

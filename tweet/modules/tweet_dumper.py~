#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import os
#Twitter API credentials
consumer_key = "YqNDEh4hARqQQx696yfNhbnXI"
consumer_secret = "N5twijhTIAeO0kuPIqgtXF3OxmJUb20CDKEVL920LvTFd65GAN"
access_key = "704396968613666816-KnUKpcmHtfDIzcY91WR4U64YVULICgc"
access_secret = "duOjLfto56GqzakEAEnWjTLQgbk6uJDCPsfXgaf6cxims"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	#new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	new_tweets = api.search(q=screen_name, count=100, lang='en')
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		#print "getting tweets before %s" % (oldest)
		try:
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=100,max_id=oldest)
		
			#save most recent tweets
			alltweets.extend(new_tweets)
		
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
		
			#print "...%s tweets downloaded so far" % (len(alltweets))
	
		except tweepy.TweepError as e:
			break
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv
	temp_data_dir = os.path.join(os.getcwd(), 'modules', 'temp_data')
	out_csv = os.path.join(temp_data_dir, '%s_tweets.csv' % screen_name)
	if os.path.isfile(out_csv):
		os.remove(out_csv)
	with open(out_csv, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets(sys.argv[1])
	print "done"

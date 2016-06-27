# Your functions go here!
import re
import json
import scipy.stats
		
"""Function to extract words from a tweet"""
def extract_words(sentence):
	word_list = re.split("[^\w\']", sentence['text']) #split sentences by word
	for word in word_list:
		if not word:
			word_list.remove(word) #Filter
	return word_list

"""Function to load sentiment data from csv file and create a dictionary of sentiments"""
def load_sentiments(file_name):
	dictionary = {}
	file = open(file_name)
	for row in file:
		row = row.strip().split(',') #remove the commas
		dictionary[row[0]] = row[1]
	return dictionary

"""Function to calculate sentiment of a string using a predefined dictionary of sentiments"""
def text_sentiment(string, dictionary):
	word_list = extract_words(string) 
	sum_of_sentiments = 0 #Var that'll hold the sum of sentiments
	for words in word_list:
		if words in dictionary:
			sum_of_sentiments = sum_of_sentiments + int(dictionary[words])
	return sum_of_sentiments

"""Function to load tweets from a source"""
def load_tweets(tweet):
	tweet_dictionary = []
	dictionary = {}
	#print(tweet)
	#tweet = open(filename) #open tweet file to read
	for json_line in tweet:
	  #json_line = json.loads(line) #get a json object from a string
	  dictionary['created_at'] = json_line['created_at']
	  dictionary['user.screen_name'] = json_line['user']['screen_name']
	  dictionary['text'] = json_line['text']
	  dictionary['retweet_count'] = json_line['retweet_count']
	  dictionary['favorite_count'] = json_line['favorite_count']
	  dictionary['hashtags'] = []
	  hash_tag_list = json_line['entities']['hashtags']
	  for value in hash_tag_list:
	   dictionary['hashtags'].append(value['text']) #picking out hashtag text to add to tweet_dictionary
	  tweet_dictionary.append(dictionary.copy())
	return tweet_dictionary

"""Function to calculate popularity of tweets"""
def popularity(filename):
  tweets = load_tweets(filename)
  retweets = 0
  favorites = 0
  for value in tweets:
    retweets += float(value['retweet_count'])
    favorites += float(value['favorite_count'])
  return (retweets / len(tweets), favorites / len(tweets)) #Return a tuple of Average number of retweets and average number of favorites

"""Function to return a hashtag count of tweets"""
def hashtag_counts(filename):
  tweets = load_tweets(filename)
  count = {}
  for counter in tweets:
    for j in counter['hashtags']:
      try:
        count[j] += 1
      except:
        count[j] = 1
  hashtags = count.items()
  hashtags_switched = [(val, key) for key, val in hashtags]
  hashtags_switched.sort(reverse = True)
  hashtags = [(val, key) for key, val in hashtags_switched]
  return hashtags

"""Creating a list of tweets with a sentiment key, value pair"""
def tweet_sentiments(tweet_list,Sentiment_file):
  #tweet_list = load_tweets(Tweet_file)
  new_tweet_list = []
  sentiment_dictionary = load_sentiments(Sentiment_file) #getting the sentiment dictionary object
  for tweet in tweet_list:
    tweet_sentiment = text_sentiment(tweet,sentiment_dictionary) #Finding the sentiment using tweet and dicitionary for reference
    tweet["sentiment"] = tweet_sentiment #assigning sentiment to a key in the tweet object
    new_tweet_list.append(tweet.copy()) 
  return new_tweet_list

"""Function to show the pearson correlation coefficient between sentiments and retweets"""
def popular_sentiment(tweet_list,Sentiment_file):
  tweet_list = []
  corr_list = []
  retweet_list = []
  sentiment_list = []
  corr_tuple = ()
  #tweet_list = tweet_sentiments(Tweet_file,Sentiment_file)
  for tweet in tweet_list:
    sentiment = float(tweet["sentiment"])
    retweet_count = float(tweet["retweet_count"])
    retweet_list.append(retweet_count)
    sentiment_list.append(sentiment)
  correlation_value = scipy.stats.pearsonr(sentiment_list,retweet_list)
  return correlation_value[0]

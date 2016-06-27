from TwitterAPI import TwitterAPI #https://github.com/geduldig/TwitterAPI
from flask import (
Flask,
request,
render_template
)
import json
from tweet_sentiments import (
load_tweets, 
load_sentiments,
text_sentiment, 
tweet_sentiments
)

#Application Configuration
app=Flask(__name__,static_url_path='')
app.config['DEBUG'] = True

# Your access information goes here
CONSUMER_KEY = "X5T8FXHks4RkWkKfCr6hfdD2F"
CONSUMER_SECRET = "8gbJMjFuZqxG4nQvJ1CV2d6qNxyQ11qvuZmUy7hugLGkoNoZ2V"
ACCESS_TOKEN_KEY = "261453877-UunAtQ33OGc1hWr7T3hCR4fnlB17O8XXLDGlcX3n"
ACCESS_TOKEN_SECRET = "Ae6WOG8oZ9XGnGCMrsiUixuXmWlOHjecBV2ZgAvjy2FJx"

#Getting an API object using the fantastic TwitterAPI python module
api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

	## "raw" stream
	#r = api.request('statuses/sample')

	## stream filtering by search term
	#r = api.request('statuses/filter', {'track': SEARCH_TERM})

"""Function to call Twitter's search API"""	
def query_twitter_search_API(SEARCH_TERM):
	tweets=[]
	## search by search term
	r = api.request('search/tweets', {'q': SEARCH_TERM, 'count':20}) #specifying search term and count of tweets obtained
	for item in r:
		if 'text' in item: #Only if it is has a text field
			tweets.append(item) 
	return tweets
	
"""Default route. Called to render Index.html"""	
@app.route('/')
def index():
	return render_template('index.html')
	
"""To handle GET request with parameters"""	
@app.route('/getData/<name>')
def aggregateTweets(name):	
	tweets=query_twitter_search_API(name) #retrieved tweets from Twitter's search API
	temp_tweets=load_tweets(tweets) #Created a list of tweet dict objects with relevant fields
	sentiments=tweet_sentiments(temp_tweets,'static/data/AFINN-111.csv') #modify passed object to add sentiment
	return json.dumps(sentiments).encode('utf8') #encoding to include international characters
	
"""Running an instance of the flask application"""
if __name__ == '__main__':
	app.run()


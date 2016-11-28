import csv
import json
import time
import tweepy
import feedparser     # available at http://feedparser.org
import sqlite3
import os.path

import getEvents
import getKeywords
import sys

##import getPersonality
##import friendRecommend

# Python version is Python 3.5.2

# You must use Python 3.0 or above
# For those who have been using python 2.7.x before, here is an article explaining key differences between python 2.7x & 3.x
# http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
	f = open(key_file)
	s = json.load(f)
	return s["api_key"],s["api_secret"], s["token"], s["token_secret"]

def getTweets(api, screen_name, no_of_tweets):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #initialize a list to hold all the tweepy Tweets
    alltweets = []	

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
    #save most recent tweets
    alltweets.extend(new_tweets)
    '''
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
	
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
		
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
	
        #save most recent tweets
        alltweets.extend(new_tweets)
		
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    '''
    #transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
    
    return outtweets
	
	
	

def getFollowers(api, root_user, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers of 'root_user'
    # rtype: list containing entries in the form of a tuple (follower, root_user)
	list=[]
	for follower in tweepy.Cursor(api.followers,screen_name=root_user).items(no_of_followers):
		list.append((follower.screen_name, root_user))
	return list
		

def getSecondaryFollowers(api, followers_list, no_of_followers):

    list=[]
    for i in range (len(followers_list)):
    	for follower in tweepy.Cursor(api.followers,screen_name=followers_list[i][0]).items(no_of_followers):
    		list.append((follower.screen_name,followers_list[i][0]))
    return list
    
    


def getFriends(api, root_user, no_of_friends):

    list=[]
    for friendid in tweepy.Cursor(api.friends_ids,screen_name=root_user).items(no_of_friends):
    	list.append((root_user,(api.get_user(friendid)).screen_name))
    return list



def getSecondaryFriends(api, friends_list, no_of_friends):

    list=[]
    for i in range (len (friends_list)):
    	for friendid in tweepy.Cursor(api.friends_ids,screen_name=friends_list[i][1]).items(no_of_friends):
    		list.append((friends_list[i][1],(api.get_user(friendid)).screen_name))
    return list
    	 


def writeToFile(data, output_file):
    # write data to output file
    # rtype: None
	writefile = open(output_file,'w',newline ='')
	writer = csv.writer(writefile)
	for line in data:
		writer.writerow(line)




def getUserInfo():
    KEY_FILE = 'keys.json'

    ROOT_USER = sys.argv[1]
    #print ROOT_USER
    NO_OF_FOLLOWERS = 10
    NO_OF_FRIENDS = 10


    OUTPUT_FILE_FOLLOWERS = 'followers.csv'
    OUTPUT_FILE_FRIENDS = 'friends.csv'
    OUTPUT_FILE_TWEETS = 'tweets_%s.txt' % ROOT_USER

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    '''
    primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
    secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)
    followers = primary_followers + secondary_followers
    
    primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)
    secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)
    friends = primary_friends + secondary_friends
    '''
    tweets = getTweets(api, ROOT_USER, NO_OF_FRIENDS)

    writeToFile(tweets, OUTPUT_FILE_TWEETS)
    #writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
    #writeToFile(friends, OUTPUT_FILE_FRIENDS)


    #--------------------Write to DB-------------------------------
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
       

    #nsert initial values into feed database
    #c.execute('DROP TABLE IF EXISTS tweets;')
    #c.execute('DROP TABLE IF EXISTS followers;')
    c.execute('CREATE TABLE IF NOT EXISTS users (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, username, CONSTRAINT name_unique UNIQUE (username))')
    c.execute('CREATE TABLE IF NOT EXISTS tweets (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, id, tweet TEXT)')
    
    
    
    
    #check for redudant username
    c.execute('INSERT INTO users (username) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?);', (ROOT_USER, ROOT_USER))
    cursor = conn.execute('SELECT entry_id from users WHERE username = (?)', (ROOT_USER,))
    for row in cursor:
       user_id = row[0]
    print(user_id)
    tweet_amount = len(tweets);

    for i in range(tweet_amount):
        c.execute('INSERT INTO tweets (id, tweet) VALUES (?,?)', (user_id, str(tweets[i])))

    conn.commit()
    print ("Records created successfully");
    conn.close()

##    #--------------------Get personality---------------------------
##    getPersonality.getPersonality(ROOT_USER)	
##    friendRecommend.friendRecommend(ROOT_USER)
	

    #----get keywords-------
    getKeywords.getKeywords(user_id)
    
    

if __name__ == '__main__':
    getUserInfo()
    getEvents.getEventInfo()
    
    

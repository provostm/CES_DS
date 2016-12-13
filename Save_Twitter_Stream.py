# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:26:07 2016

@author: martin.provost
"""

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy.auth import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'H7XKrTUW2FhKbe41Qf20AL5VX'
consumer_secret = 'eRa1TqE0J26hhqaDyAkztctpdL3wnnNOnnFuJNsusKiGjIAqdh'
access_token = '798100114007064576-42y4esKrGwcuJNQ4RvX13a9xw8folJi'
access_token_secret = 'tETGgYe7LK5lQvNAxngS2K4cYho8NqNdaEFEsrn8aRilf'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 
    stream.filter(track=['datascience'])
    
    
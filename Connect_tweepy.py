# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 10:22:10 2016

@author: martin.provost
"""

from tweepy.auth import OAuthHandler
from tweepy import API
import json
import pandas as pd

def TweepyConnect():
# se connecter à apps.twitter.com et aller dans le menu de l'application en question
# nom de l'application twitter : 'API familiariser Tweets'
# Consumer keys and access tokens, used for OAuth
    consumer_key = 'H7XKrTUW2FhKbe41Qf20AL5V'
    consumer_secret = 'eRa1TqE0J26hhqaDyAkztctpdL3wnnNOnnFuJNsusKiGjIAqd'
    access_token = '798100114007064576-42y4esKrGwcuJNQ4RvX13a9xw8folJ'
    access_token_secret = 'tETGgYe7LK5lQvNAxngS2K4cYho8NqNdaEFEsrn8aRil'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = API(auth)
    
#    print(api.me().name + ' from connect_tweepy')
    return api


#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print tweet.text
 


#liste_name_followers=[]
#for follow in followers:
#    liste_name_followers.append( follow.screen_name)
#print liste_name_followers

#print user.screen_name
#print "nombre de followers : "+ str( user.followers_count)
#print "nombre d'abonnements : " + str( len(user.friends()) )
#for friend in user.friends():
#   if friend.screen_name<> '': print friend.screen_name


def dict_to_df(d):
    df=pd.DataFrame(d.items())
    df.set_index(0, inplace=True)
    return df.T


# requeter des tweets contenant le mot 'hadoop' et qui sont en langue française
def keyWordsSearch(api, keyWords='', langue='fr', rpp=100, maxTweets=1000, geocode=None, radius=None):
    
    tweets = api.search(q=keyWords, lang=langue, rpp=rpp, count=maxTweets, geodcode=geocode,radius=radius)
#    tweets.filter()
#    dic={} # dictionnaire qui va contenir les informations utiles de la recherche    
   
#    for tweet in tweets:
#        id_tweet=tweet.id
#        dic["author"]=tweet.author.screen_name        
#        dic["create_date"]= tweet.created_at
#        dic["author_location"]= tweet.user.location
#        dic["full_name"]= tweet.user.name
#        dic["text"]=tweet.text
    
    df=pd.DataFrame()
    i=0
    for tweet in tweets:
#        id_tweet=tweet.id
        dic={}
        dic["author"]=tweet.author.screen_name
        dic["create_date"]= tweet.created_at
        dic["author_location"]= tweet.user.location
        dic["full_name"]= tweet.user.name
        dic["text"]=tweet.text.encode('utf-8')
        dic["id_tweet"]=tweet.id
#        dic["Tweet_location"]= tweet.place.name
        
        
        df=df.append(dict_to_df(dic))
        
#        df["author"]=tweet.author.screen_name        
#        df["create_date"]= tweet.created_at
#        df["author_location"]= tweet.user.location
#        df["full_name"]= tweet.user.name
#        df["text"]=tweet.text
        
#    df.set_index("id_tweet")   
    return df

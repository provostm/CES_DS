# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 10:22:10 2016

@author: martin.provost
"""

from tweepy.auth import OAuthHandler
from tweepy import API
import tweepy
import pandas as pd

def TweepyConnect():
# se connecter à apps.twitter.com et aller dans le menu de l'application en question
# nom de l'application twitter : 'API familiariser Tweets'
# Consumer keys and access tokens, used for OAuth
    consumer_key = 'H7XKrTUW2FhKbe41Qf20AL5VX'
    consumer_secret = 'eRa1TqE0J26hhqaDyAkztctpdL3wnnNOnnFuJNsusKiGjIAqdh'
    access_token = '798100114007064576-42y4esKrGwcuJNQ4RvX13a9xw8folJi'
    access_token_secret = 'tETGgYe7LK5lQvNAxngS2K4cYho8NqNdaEFEsrn8aRilf'

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
def keyWordsSearch(api, keyWords='', langues='', rpp=1000, maxTweets=1000, geocode=None, radius=None, retweet=True, result_type='mixed', limit_retweets=0):
    
#    tweets = api.search(q=keyWords, lang=langue, rpp=rpp, count=1000, result_type=result_type)
    
#    tweets = [status for status in tweepy.Cursor(api.search, q=keyWords, lang=langue, rpp=rpp, geodcode=geocode,radius=radius).items(500)]
#    print len(tweets)

    df=pd.DataFrame()
    
#    while(df.shape[0] < maxTweets):
    for langue in langues:
        for tweets in tweepy.Cursor(api.search, q=keyWords, lang=langue, geodcode=geocode,radius=radius, result_type=result_type).pages():
    #        print u"La requête totale peut ramener " +str(len(tweets)) +" tweets.\n"
            for tweet in tweets:
                if df.shape[0] >= maxTweets: # si on atteint le nombre de tweets voulus
                    return df
        #        id_tweet=tweet.id
                 
                dic={}
                dic["author"]=tweet.author.screen_name
                dic["create_date"]= tweet.created_at
                dic["author_location"]= tweet.user.location
                dic["full_name"]= tweet.user.name
                text=tweet.text.encode('utf-8')
                dic["text"]=text
                dic["id_tweet"]=tweet.id
                retweet_count = tweet.retweet_count
                dic["retweet_count"]=retweet_count
                dic["lang"]=tweet.user.lang
                dic["iso_lang"]=tweet.metadata["iso_language_code"]
                
        #        dic["Tweet_location"]= tweet.place.name
                
                if retweet:
                    if retweet_count > limit_retweets and text[0:2] != "RT":
                        df=df.append(dict_to_df(dic))
                else:
                    df=df.append(dict_to_df(dic))
        
    return df

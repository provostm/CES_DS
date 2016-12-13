# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:08:54 2016

@author: martin.provost
"""

import oauth2 as oauth
import urlparse

consumer_key           = "7724vt213ze2m"
consumer_secret        = "GVd9MjBigin3yQh"

oauth_token        = "df4fdee1-9a37-447d-a51f-7a049a98526"
oauth_token_secret = "4d1301e0-4c2a-40a3-9971-8d822ca59ac"

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

request_token_url      = 'https://api.linkedin.com/uas/oauth/requestToken'
resp, content = client.request(request_token_url, "POST")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])

print content
print "\n"

request_token = dict(urlparse.parse_qsl(content))

print "Requesr Token:",  "\n"
print "- oauth_token        = %s" % request_token['oauth_token'], "\n"
print "- oauth_token_secret = %s" % request_token['oauth_token_secret'], "\n"

authorize_url = 'https://api.linkedin.com/uas/oauth/authorize'
print "Go to the following link in your browser:", "\n"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']), "\n"

accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')

access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content))

print "Access Token:", "\n"
print "- oauth_token        = %s" % access_token['oauth_token'], "\n"
print "- oauth_token_secret = %s" % access_token['oauth_token_secret']
print "You may now access protected resources using the access tokens above."

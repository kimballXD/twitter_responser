# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 23:58:26 2019

@author: Wu
"""

import tweepy
from flask import Flask, redirect, request, session
import yaml
app = Flask(__name__)


#%%

with open('config.yaml', 'r') as cf:
    config = yaml.load(cf)

api_key = config['api'][0]['api_key']
api_secret = config['api'][0]['api_secret_key']

# change this setting after deployeeee!
url_dict = config['collector']
callback = '{protocol}://{ip}:{port}{token_endpoint}'.format(**url_dict)

db_path = config['token_db_path']
token_message = """
<H1>We have recieve your authorization, thank you!</H1>
<p style="font-size:24px">Your twitter authorization information:</p>
<p style="font-size:24px">Access Token = {}</p>
<p style="font-size:24px">Access Secret = {}</p>
"""

#%%
@app.route('/')
def hello():
    return "<H1>Please reply the deployed server ip + port!</H1>"

@app.route(url_dict['auth_endpoint'])
def auth():
    auth = tweepy.OAuthHandler(api_key, api_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token['oauth_token']
    return redirect(url)

@app.route(url_dict['token_endpoint'])
def show_tokens():
    request_token = session['request_token']
    del session['request_token']    
    auth = tweepy.OAuthHandler(api_key, api_secret, callback)
    verifier = request.args.get('oauth_verifier') 
    auth.request_token = {'oauth_token' : request_token,
                          'oauth_token_secret' : verifier }        
    auth.get_access_token(verifier)
    info = [auth.access_token, auth.access_token_secret]
    with open(db_path,'a') as db:
        db.write(','.join(info))
        db.write('\n')
    return token_message.format(*info)


if __name__ == '__main__':
    app.secret_key = 'iinenene'
    app.run(host='0.0.0.0', port = url_dict['port'])
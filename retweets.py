# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 22:00:36 2019

@author: Wu
"""
import tweepy
import yaml
import sqlite3
with open('config.yaml', 'r') as cf:
    config = yaml.load(cf)

#%% generate user list
with open(config['token_db_path'], 'r') as tdb:
    tokens = set(tdb.read().strip().split('\n'))
    tokens = [t.split(',') for t in tokens]

#%% get api instance using specific user

api_key = config['api'][0]['api_key']
api_secret = config['api'][0]['api_secret_key']
auth = tweepy.OAuthHandler(api_key, api_secret)
conn = sqlite3.connect(config['db_path'])
cur = conn.cursor() 

error_cnt= 0
success_cnt = 0
# for every user
for token, secret in tokens[:1]:    
    # init api
    auth.set_access_token(token, secret)    
    api = tweepy.API(auth)
    name = api.me().screen_name
    #%% get all retweets for given user
    retweets = cur.execute('select tweet_id from retweets where uid = "{}"'.format(name))
    retweets = set([r[0] for r in retweets.fetchall()])
    
    #%% retweet new tweets of track user
    for tuid in config['track_uid']:        
        tweets = api.user_timeline(screen_name = tuid, count =config['latest'],)
        tweets = set([t.id_str for t in tweets])        
        new = tweets.difference(retweets)
        
        # action for new tweets
        success = []
        for tid in new:
            try:
                tmp = api.retweet(tid)
                tmp2 = api.create_favorite(tid)
                success_cnt = success_cnt + 1 
                success.append(tid)
            except Exception as e:
                if e.api_code == 327:
                    success.append(tid)
                error_cnt = error_cnt +1
            
        # udpate db
        insert = [(name, tid) for tid in success]
        cur.executemany('INSERT INTO retweets VALUES(?,?)', insert)
        conn.commit()

#%%
conn.close()        
print('Retweet Job Finished!: Success count {}, Error count {}'.format(
        success_cnt, error_cnt))
    
    
    
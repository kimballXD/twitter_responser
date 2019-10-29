# "iine" Twitter bot

An bot that help users to response to their favorite authors' tweets. It spread smile and love on Twitter. It's a nice bot!

## Environment

​	Python 3.7 with the following 3rd party library dependency:

- flask (for the advance use only)
- tweepy
- yaml

## Usage

1. Apply for a Twitter Developer account and create a Twitter App project.  Get the <u>API key</u> and <u>API secret key</u>  from the project page (follow the [steps](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens) here), then add those information into `config.yaml`. 
2.  Let's say you want to use the current developer account to response to other people. In this case, you can generate <u>access token</u> and <u>access token secret</u> for your current account in the same page you just generate API key and API secret key.  Generate access token and access token secret and add them to `token_db.csv` in the format of `{access token},{access token secret}`; one account authorization in a line.
3. Add the twitter accounts which your want to response to their tweets into `config.yaml`.  Copy the @username (name **after** "@", e.g., realDonaldTrump for [Donald Trump](https://twitter.com/realdonaldtrump)) and put it in the list called `track_uid`. 
4. Response to the tweets automatically with `Responser`scripts by simply execute the following `Responser` script in command line.
5. - `retweet.py`: **retweet** newest 10 tweets post by `track_uids`to your twitter account. 

## Advance Use: collect user authorization through the web

This library comes with a `flask` script that help you to collect user authorization (i.e., access token and access token secret) from users using  web interface. To use this flask script, do the following:

1. Deploy the `token_collect.py` to web server, then add the information of the protocol(e.g.: http/https), ip/domain name, and port into `config.yaml`.
2. Determine the API endpoint which Twitter will respond to the endpoint with user's authorization information after user has authorized your Twitter app. Set this endpoint as `token_endpoint` in `config.ymal`, and add the full endpoint URL to your Twitter API  as the  `Callback URL` 
3. Determine the API endpoint which user will access to it and start to make authorization. Set this endpoint as `auth_endpoint` in `config.ymal`.
4. That's all! Send the full `auth_endpoint` URL to your user.  When user access to `auth_endpoint`, browser will first redirect users to Twitter to make the authorization, then redirect them back to your `token_endpoint`.  `tocken_collect.py` script will automatically write the authorization information into a local file `token_db.csv`.
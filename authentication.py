import tweepy

__consumer_key = ""
__consumer_secret = ""
__access_token = ""
__access_token_secret = ""


def authenticate(key=__consumer_key, secret=__consumer_secret, token=__access_token, token_secret=__access_token_secret):

    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    return auth, api

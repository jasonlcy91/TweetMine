import tweepy

__consumer_key = "Ha1yKss6mHdGpKxPdKRDCnG1X"
__consumer_secret = "K9P3wazVVbM40lHQPBRQWmJAZwoqo1LU3DoCkfuCLTD3WTsyJ3"
__access_token = "268674910-SZIl1DB0k0FbVSSANQHJXgdCJyzCi7Qibz87bDSz"
__access_token_secret = "zFVTO3ofaF1YYHGXsvVWO4uBd7QCwpFe1G3r0qYtIsyXf"


def authenticate(key=__consumer_key, secret=__consumer_secret, token=__access_token, token_secret=__access_token_secret):

    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    return auth, api

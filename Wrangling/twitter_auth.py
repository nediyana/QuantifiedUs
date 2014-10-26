import twitter

def oauth_login():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information 
    # on Twitter's OAuth implementation.
    
    CONSUMER_KEY = 'Z0Z6FGS09KhNg9ceqvkEQ6Vbe'
    CONSUMER_SECRET = 'tWw3pgXeQFoWahquk6PqZXJQP0otj0cRb0Zbu1KEL9MyK7qsRH'
    OAUTH_TOKEN = '25219647-yTdfUkMCTcUqrJTpGXke2jxiG3QCL2bjo2oWHrOzt'
    OAUTH_TOKEN_SECRET = 'cgk7aE3KRJX5bnVTMh8iPYQYevfg3PZ1VUb9J9XzPjd0K'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

# Sample usage
ta = oauth_login()    


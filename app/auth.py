import os
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


client_id = os.environ['BLACKBOARD_SECRET_KEY']  #Configuration.BLACKBOARD_SECRET_KEY
client_secret = os.environ['BLACKBOARD_SECRET_SECRET'] #Configuration.BLACKBOARD_SECRET_SECRET
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token_url_path = 'https://blackboard-staging.test.ualr.edu/learn/api/public/v1/oauth2/token'

def getToken():

    try:

        token = oauth.fetch_token(token_url=token_url_path, client_id=client_id, client_secret=client_secret)
        blackboard_access_token = token['access_token']
        authStr = 'Bearer ' + blackboard_access_token

        return authStr

    except KeyError as e:
        print(e)






getToken()
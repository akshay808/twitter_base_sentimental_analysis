import oauth2 as oauth
import urllib2 as urllib
from config import *
import os

api_key = "YqNDEh4hARqQQx696yfNhbnXI"
api_secret = "N5twijhTIAeO0kuPIqgtXF3OxmJUb20CDKEVL920LvTFd65GAN"
access_token_key = "704396968613666816-KnUKpcmHtfDIzcY91WR4U64YVULICgc"
access_token_secret = "duOjLfto56GqzakEAEnWjTLQgbk6uJDCPsfXgaf6cxims"


_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "POST"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                               token=oauth_token,
                                               http_method=http_method,
                                               http_url=url, 
                                               parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def fetchsamples(word, loc1, loc2):
    #url = "https://stream.twitter.com/1.1/statuses/filter.json?track=modi&locations=51.6194732,-0.0975131,52.6194732,-0.0475131"
    url = "https://stream.twitter.com/1.1/statuses/filter.json?track=%s&locations=%s,%s,%s,%s,"%(word, loc1[0], loc1[1], loc2[0], loc2[1])
    parameters = []
    response = twitterreq(url, http_method, parameters)
    
    #write the csv
    temp_data_dir = os.getcwd()
    out_csv = os.path.join(temp_data_dir, '%s_india_tweets.csv' % word)
    if os.path.isfile(out_csv):
      os.remove(out_csv)
    with open(out_csv, 'wb') as f:
      print dir(response)
      for line in response:
        f.write(line.strip())
      

if __name__ == '__main__':
    fetchsamples('modi', ["18.5204", "73.8567"], ["22.5726", "88.3639"])
from twython import Twython

from jaffucci import app

TWIT_APP_KEY = app.config["TWIT_APP_KEY"]
TWIT_APP_SECRET = app.config["TWIT_APP_SECRET"]
TWIT_ACCESS_TOKEN = app.config["TWIT_ACCESS_TOKEN"]
TWIT_ACCESS_SECRET = app.config["TWIT_ACCESS_SECRET"]

twitter = Twython(TWIT_APP_KEY, TWIT_APP_SECRET, TWIT_ACCESS_TOKEN, TWIT_ACCESS_SECRET)

def get_media_url(item):
    try:
        return item['entities']['media'][0]['media_url']
    except:
        return None


def get_img_urls(user):
    status_list = twitter.get_user_timeline(user_id=user)
    media_urls = map(get_media_url, status_list)
    return [ a for a in media_urls if a != None ]

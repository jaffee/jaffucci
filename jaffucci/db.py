import pymongo
from jaffucci import app

dbname = app.config['DBNAME']

c = pymongo.MongoClient()
db = c[dbname]

if not db["users"].find_one():
    db["users"].save({"user_id": "matt", "password": "blahh"})

def get_user(**kwargs):
    return db["users"].find_one(kwargs)

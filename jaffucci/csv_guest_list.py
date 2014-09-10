import pymongo
import sys
import csv
from docopt import docopt
if __name__ != "__main__":
    from jaffucci import app
    from jaffucci import db
else:
    sys.path = [sys.path[0]+"/.."] + sys.path
    from jaffucci import app
    from jaffucci import db


cli = pymongo.MongoClient()

db = cli["policydb"]

groups = db["rsvpgroups"].find()

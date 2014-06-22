#!/usr/bin/python
"""
Usage:
  db_admin.py cp [options] <target_name>
  db_admin.py rm <db_to_remove>
  db_admin.py rm_coll <collection_to_remove>
  db_admin.py import_guests <filename>

Options:
  --dbname <dbname>
"""
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

def main(args):
    if args["--dbname"]:
        dbname = args["--dbname"]
    else:
        dbname = app.config["DBNAME"]

    cli = pymongo.MongoClient()
    if args["cp"]:
        ret = cli.copy_database(dbname, args["<target_name>"], "localhost")
        print ret

    elif args["rm"]:
        print "Going to remove " + args["<db_to_remove>"] + " ...are you sure (yes/no)?"
        a = None
        while not a:
            a = raw_input()
            if a == "yes":
                ret = cli.drop_database(args["<db_to_remove>"])
                print "dropped " + args["<db_to_remove>"]
                return
            elif a == "no":
                return
            else:
                print "Please type yes or no"
                a = None

    elif args["rm_coll"]:
        print "Going to remove Collection: " + args["<collection_to_remove>"] + " ...are you sure (yes/no)?"
        yes_no_guard(cli[dbname].drop_collection, args["<collection_to_remove>"])

    elif args["import_guests"]:
        import_guests(args["<filename>"])

def yes_no_guard(f, *args, **kwargs):
    a = None
    while not a:
        a = raw_input()
        if a == "yes":
            ret = f(*args, **kwargs)
            print "returned " + str(ret)
            return
        elif a == "no":
            return
        else:
            print "Please type yes or no"
            a = None


def import_guests(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        print reader.next()
        group = None
        for row in reader:
            if row[1]:
                if group:
                    db.groups.save(group)
                group = {
                    "code": row[1],
                    "display-name": row[0].split()[-1],
                    "guest-names": [row[0]],
                }
            else:
                group["guest-names"].append(row[0])
            guest = {
                "name": row[0],
                "coming": "",
                "entree": "",
            }
            db.guests.save(guest)

# class UnicodeCsvReader(object):
#     def __init__(self, f, encoding="utf-8", **kwargs):
#         self.csv_reader = csv.reader(f, **kwargs)
#         self.encoding = encoding

#     def __iter__(self):
#         return self

#     def next(self):
#         # read and split the csv row into fields
#         row = self.csv_reader.next()
#         # now decode
#         return [unicode(cell, self.encoding) for cell in row]

#     @property
#     def line_num(self):
#         return self.csv_reader.line_num

# class UnicodeDictReader(csv.DictReader):
#     def __init__(self, f, encoding="utf-8", fieldnames=None, **kwds):
#         csv.DictReader.__init__(self, f, fieldnames=fieldnames, **kwds)
#         self.reader = UnicodeCsvReader(f, encoding=encoding, **kwds)

if __name__ == "__main__":
    args = docopt(__doc__)
    for a in args:
        print a + " = " + str(args[a])
    main(args)

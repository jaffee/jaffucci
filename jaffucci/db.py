import pymongo
from jaffucci import app

dbname = app.config['DBNAME']

c = pymongo.MongoClient()
db = c[dbname]
guests = db["guests"]
groups = db["rsvpgroups"]
selfies = db["selfies"].find_one()
if not selfies:
    db["selfies"].save({"pic_urls": []})
    selfies = db["selfies"].find_one()

def startup():
    if not db["users"].find_one():
        db["users"].save({"user_id": "matt", "password": "blahh"})


    # if not db["guests"].find_one() and not db["rsvpgroups"].find_one():
    #     dguest = {"name": "Johnson O'leary",
    #               "entree": "",
    #               "coming": ""}
    #     dgroup = {
    #         "guest-names": ["Johnson O'leary"],
    #         "code": "fjdksla;",
    #         "display-name": "O'leary"
    #     }
    #     db["guests"].save(dguest)
    #     db["rsvpgroups"].save(dgroup)

    # add_guest("Helena O'leary", "O'leary")


def get_user(**kwargs):
    return db["users"].find_one(kwargs)


def add_guest(name, group_display_name=None, ignore_exists=True):
    # won't handle multiple guests with the same name
    guest = guests.find_one({"name": name})
    if not guest:
        guest = {
            "name": name,
            "entree": "",
            "coming": ""
        }
        guests.save(guest)
    elif not ignore_exists:
        raise GuestExistsError(name)
    if group_display_name:
        move_guest_to_group(guest, group_display_name)


def move_guest_to_group(guest, group_display_name):
    name = guest["name"]
    allgroups = groups.find({"guest-names": name})
    for g in allgroups:
        if not g["display-name"] == group_display_name:
            g["guest-names"].remove(name)
            groups.save(g)

    group = groups.find_one({"display-name": group_display_name})
    if not group:
        raise UnknownGroupError(group_display_name)

    if name in group["guest-names"]:
        return
    group["guest-names"].append(name)
    groups.save(group)

def update_pic_urls(pic_urls):
    saved_urls = selfies["pic_urls"]
    all_urls = list(set(pic_urls + saved_urls))
    selfies["pic_urls"] = all_urls
    db["selfies"].save(selfies)

def get_pic_urls():
    return selfies["pic_urls"]


class UnknownGroupError(Exception):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return repr(self.e)

class GuestExistsError(Exception):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return repr(self.e)

class DuplicateGuestNameError(Exception):
    '''The DuplicateGuestNameError occurs when a guest does not exist for
       a certain name, but that name already exists in a group's guest-names
       list'''
    def __init__(self, name, groupdisplayname):
        self.name = name
        self.groupdisplayname = groupdisplayname
    def __str__(self):
        return "Guest: " + self.name + " Group: " + self.groupdisplayname


startup()

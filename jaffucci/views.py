from jaffucci import app, forms, user
import jaffucci.db as db # import db
from flask import redirect, render_template, url_for, flash, request, session
from werkzeug import secure_filename
import os
import requests
from get_img_urls import get_img_urls


from flask_mail import Mail, Message
from flask_login import (login_user, logout_user, flash, login_required,
                         LoginManager, current_user)
from pprint import pprint
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#app.secret_key = app.config['SECRET_KEY']
TWIT_USER = app.config['TWIT_USER']

pprint(app.config)

mail = Mail(app)

def normalize_password(apass):
    return apass.strip().replace(" ", "").lower()



@login_manager.user_loader
def load_user(user_id):
    return user.User(user_id)
    return None


@app.route('/')
def index():
    # if not session.get('rsvpd?', None):
    #     return redirect(url_for('rsvp'))
    # else:
    return redirect(url_for('home'))

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    form = forms.RSVPForm()
    if form.validate_on_submit():
        code =  normalize_password(form.password.data)
        group = db.groups.find_one({"code": code})
        if group:
            session['rsvp-code'] = code
            return redirect(url_for('rsvp_form'))
        else:
            flash("Sorry! We don't have that password on file - check your spelling and try again. <br/> If you continue to have trouble, <a href='forgot_password'> click here</a>")
    return render_template("rsvp.html",
                           selected={}, form=form)

@app.route('/selfies')
def selfies():
    try:
        pic_urls = get_img_urls(TWIT_USER)
        db.update_pic_urls(pic_urls)
    except:
        pic_urls = db.get_img_urls()
    return render_template("selfies.html",
                           selected={},
                           pic_urls=pic_urls)

@app.route("/rsvp_form", methods=['GET', 'POST'])
def rsvp_form():
    class F(forms.RSVPDetailForm):
        pass
    group = db.groups.find_one({"code": session['rsvp-code']})
    guests = db.guests.find({"name": {"$in": group["guest-names"]}})
    guests = [gr for gr in guests]
    form = F.get(guests)
    if form.validate_on_submit():
        post_url = "https://api.mailgun.net/v2/" + app.config["MAILGUN_DOMAIN"] + "/messages"
        auth = ("api", app.config["MAILGUN_API_KEY"])
        data = {"subject": "RSVP - " + group['display-name'] + " " + session['rsvp-code'],
                "from": "sidama@jaffucci.com",
                "text": "",
                "to": app.config["RECIPIENTS"]}
        group["comment"] = form.comment.data
        db.groups.save(group)

        for gr in guests:
            gr["entree"] = form["entree_" + gr["name"]].data
            gr["coming"] = form["yesno_" + gr["name"]].data
            data["text"] += "RSVP: " + gr["name"] + " " + gr["coming"] + " " + gr["entree"] + "\n"
            db.guests.save(gr)
        data["text"] += "\nComment:\n" + group.get("comment", "")
        requests.post(post_url, auth=auth, data=data)
        session['rsvpd?'] = True
        return redirect(url_for("rsvp_done"))

    if request.method == "GET":
        form.fill_in(guests, group)
    return render_template("rsvp_form.html", group=group, guests=guests, form=form, selected={})

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html", selected={})

@app.route("/rsvp_done")
def rsvp_done():
    group = db.groups.find_one({"code": session['rsvp-code']})
    guests = db.guests.find({"name": {"$in": group["guest-names"]}})
    guests = [g for g in guests]

    return render_template("rsvp_done.html", guests=guests, group=group, selected={})


@app.route('/home')
def home():
    return render_template("home.html",
                           title="Debbie and Matt",
                           selected={})


@app.route('/event_information')
@app.route('/event_information/<string:subpage>')
def event_information(subpage=None):
    return render_template("event_information.html",
                           title="Event Info",
                           subpage=subpage,
                           selected={"event_information": "selected"})

@app.route('/accomodations/<string:subpage>')
@app.route('/accomodations')
def accomodations(subpage=None):
    return render_template("accomodations.html",
                           subpage=subpage,
                           title="Accomodations",
                           selected={"accomodations": "selected"})

@app.route('/our_story')
def our_story():
    return render_template("our_story.html",
                           title="Our Story",
                           selected={"our_story": "selected"})

@app.route('/happy_hour')
def happy_hour():
    return render_template("happy_hour.html",
                           title="Happy Hour",
                           selected={"happy_hour": "selected"})

@app.route('/images', methods=['GET', 'POST'])
def images():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file")
    print uploaded_files
    filenames = []
    for f in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if f:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(f.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return redirect(url_for('happy_hour'))


@app.route('/image_check')
@login_required
def image_check():
    upload_dir = app.config["UPLOAD_FOLDER"]
    images = os.listdir(upload_dir)
    return render_template("image_check.html",
                           title="Image Check",
                           images=images,
                           selected={})

@app.route('/rsvp_check')
@login_required
def rsvp_check():
    guests = [g for g in db.guests.find()]
    groups = [b for b in db.groups.find()]
    return render_template("rsvp_check.html", guests=guests, groups=groups)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        u_obj = db.get_user(user_id=form.user_id.data, password=form.password.data)
        if not u_obj:
            flash("User id/password not found")
        else:
            login_user(load_user(u_obj["user_id"]))
            flash("login success")
            return redirect(request.args.get("next") or url_for("home"))

    return render_template("login.html",
                           selected={},
                           form=form)

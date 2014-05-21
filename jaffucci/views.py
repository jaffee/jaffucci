from jaffucci import app, forms, user, db
from flask import redirect, render_template, url_for, flash, request, g, send_from_directory
from werkzeug import secure_filename
import os


from flask_login import (login_user, logout_user, flash, login_required,
                         LoginManager, current_user)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#app.secret_key = app.config['SECRET_KEY']



@login_manager.user_loader
def load_user(user_id):
    return user.User(user_id)
    return None


@app.route('/')
def index():
    return redirect(url_for('home'))


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

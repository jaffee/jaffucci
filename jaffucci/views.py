from jaffucci import app, forms, user, db
from flask import redirect, render_template, url_for, flash, request, g


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
def event_information():
    return render_template("event_information.html",
                           title="Event Info",
                           selected={"event_information": "selected"})

@app.route('/accomodations')
def accomodations():
    return render_template("accomodations.html",
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

@app.route('/image_check')
@login_required
def image_check():
    return "super secret", 200


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
                           form=form)

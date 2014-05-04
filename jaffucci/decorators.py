from flask_login import current_user
from flask import flash, redirect, url_for
from functools import wraps

def admin_required(f):
    @wraps(f)
    def insidefunc(*args, **kwargs):
        if hasattr(current_user, "is_admin") and current_user.is_admin():
            return f(*args, **kwargs)
        else:
            flash("You are not authorized to view this page")
            return redirect(url_for("index"))
    return insidefunc

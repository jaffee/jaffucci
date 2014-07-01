from flask_wtf import Form
from wtforms import (TextField, RadioField, SelectField, SelectMultipleField,
                     IntegerField, PasswordField, TextAreaField)
from wtforms.validators import Required, EqualTo, NumberRange, Email, Optional, ValidationError


class DynamicForm(Form):
    @classmethod
    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls


class LoginForm(Form):
    user_id = TextField('userid',
                        validators=[Required()])
    password = PasswordField('password',
                             validators=[Required(message="Password Required")])


class RSVPForm(Form):
    password = TextField('password', validators=[Required(message="Please enter the password from your invitation")])


def required_if_other_equals(otherfieldname, otherval, message=""):
    def _r(form, field):
        if field.data:
            return True
        else:
            if form[otherfieldname].data == otherval:
                raise ValidationError(message)
            return True
    return _r

class RSVPDetailForm(DynamicForm):
    comment = TextAreaField('comment')
    @classmethod
    def get(cls, guests):
        for g in guests:
            name = g["name"]
            cls.append_field('yesno_' + name,
                           SelectField('Attendance', choices=[
                               ("", "<Select Attendance>"),
                               ("yes", "joyfully accepts"),
                               ("no", "regretfully declines")],
                                       validators=[Required()]))
            cls.append_field('entree_' + name,
                           SelectField('Entree', choices=[
                               ("", "<Select Entree>"),
                               ("meat", "Duet of Filet Mignon and Crabcake"),
                               ("veg", "Vegan Raviolis")],
                                       validators=[required_if_other_equals("yesno_" + name,
                                                                            "yes",
                                                                            "If you are attending, please select an entree")]))
        return cls()

    def fill_in(self, guests, group):
        self["comment"].data = group.get("comment", "")
        for g in guests:
            name = g["name"]
            self["yesno_" + name].data = g["coming"]
            self["entree_" + name].data = g["entree"]


    # yesno = SelectField('yesno', choices=[("yes", "joyfully accepts"),
    #                                       ("no", "regretfully declines")],
    #                     validators=[Required()])
    # entree = SelectField('entree', choices=[("meat", "Duet of X and X"),
    #                                         ("veg", "Vegeterian Option")],
    #                      validators=[Required()])

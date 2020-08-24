from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import json
class signup_form(FlaskForm):
    name = StringField("Username")
    pw = StringField("Password")
    submit = SubmitField("click to signup")

class login_form(FlaskForm):
    name = StringField("Username")
    pw = StringField("Password")
    submit = SubmitField("click to login")



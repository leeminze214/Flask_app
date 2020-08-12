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

def update_database(data):
    with open("db.json",'w') as f:
        json.dump(data, f)
def open_db():
    with open("db.json") as f:
        return json.load(f)

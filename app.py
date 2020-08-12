from flask import Flask, request,render_template, redirect, url_for, session,flash
#session works like a cookie
#flask-login would be used for login/authentication
from forms import signup_form, update_database, login_form, open_db
from datetime import timedelta
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=3)
app.config["SECRET_KEY"] = "hellnah"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

#data table models to store user login info and Score
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) #meaning will be the identification column
    name = db.Column(db.String, index = True) #index allows reference by value
    pw = db.Column(db.String, unique = False)
    user_scores = db.relationship('Score', backref = 'user', uselist=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#https://softwareengineering.stackexchange.com/questions/262141/is-it-a-bad-choice-to-consume-the-rest-api-from-the-back-end-too
#https://stackoverflow.com/questions/58833714/how-does-an-api-compare-to-directly-querying-your-database
@app.route("/")
def index():
    score = None
    if 'name' in session:
        session["score"] += 1
        updating = Score.query.filter_by(user_id = session['user_id']).first()
        updating.score = session['score']
        db.session.commit()
        score = session["score"]
#    test = user.query.filter_by(name="d4f").first()
    test = User.query.all()
    return render_template('index.html', score = score,test = test)

@app.route("/signup", methods=["Get","Post"])
def signup():
    form = signup_form()
    if "name" in session:
        flash("To sign up for new account, you would have to log out first.")
        return redirect(url_for("games"))
    if form.validate_on_submit():
        name = form.name.data
        pw = form.pw.data
        account = User.query.filter_by(name = name).first()
        if account:
            if account.pw == pw:
                flash("This account exists, try logging in.")
                return redirect(url_for("login"))
            flash(f"{name} already exists, try another username")
            return redirect(url_for("signup"))
        else:
            new_user = User(name = name, pw = pw)
            db.session.add(new_user)
            db.session.commit()
            new_score = Score(score = 0, user_id = new_user.id)
            db.session.add(new_score)
            db.session.commit()
            flash("You have successfully signed up, now try logging in")
            return redirect(url_for("login"))
    return render_template("signup.html", acc_form = form)

@app.route("/login" ,methods = ["Get", "Post"])
def login():
    form = login_form()
    if "name" in session:
        flash("You are already logged in")
        return redirect(url_for("games"))
    elif form.validate_on_submit():
        name = form.name.data
        pw = form.pw.data
        validate_login = User.query.filter_by(name = name, pw = pw).first()
        if validate_login:
            session.permanent = True
            session["name"] = validate_login.name
            session['user_id'] = validate_login.id
            session['score'] = validate_login.user_scores.score

            flash("Login successful, Master " + name)
            return redirect(url_for('games'))
        flash("Invalid login! Try again.")
        return redirect(url_for('login'))
    return render_template('login.html', acc_form = form)

@app.route("/games")
def games():
    name = None
    score = None
    if "name" in session:
        name = session["name"]
        score = session["score"]
    else:
        flash("Reminder: You can login to keep track of your records!!")
    return render_template("games.html", name = name, score = score)

@app.route("/logout", methods=["Get","Post"])
def logout():
    if "name" not in session:
        flash("You have not logged in yet")
        return redirect(url_for("login"))
    name = session["name"]
    pw = None
    if "password" in request.form:
        pw = request.form["password"]
    validate_logout = User.query.filter_by(name = name, pw = pw).first()
    if validate_logout:
        flash("You have successfully logged out")
        session.pop("name", None)
        session.pop("score", None)
        session.pop("user_id", None)
        return redirect("/")
    return render_template("logout.html", name = name)
if __name__ == '__main__':
    app.run(debug=True)

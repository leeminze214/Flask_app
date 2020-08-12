'''from flask import Flask, request,render_template, redirect, url_for, session,flash
#session works like a cookie
#flask-login would be used for login/authentication
from forms import signup_form, update_database, login_form, open_db
from datetime import timedelta
import json

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=3)
app.config["SECRET_KEY"] = "hellnah"
#https://softwareengineering.stackexchange.com/questions/262141/is-it-a-bad-choice-to-consume-the-rest-api-from-the-back-end-too
#https://stackoverflow.com/questions/58833714/how-does-an-api-compare-to-directly-querying-your-database
@app.route("/")
def index():
    count = None
    if "count" in session:
        session["count"] +=1
        count = session["count"]
    return render_template('index.html', count = count)

@app.route("/signup", methods=["Get","Post"])
def signup():
    form = signup_form()
    if "name" in session:
        flash("To sign up for new account, you would have to log out first.")
        return redirect(url_for("user_dashboard"))
    if form.validate_on_submit():

        name = form.name.data
        pw = form.pw.data
        all = open_db()

        if all.get(name) != None:
            if all[name] == pw:
                flash("This account exists, try logging in.")
                return redirect(url_for("login"))
            flash(f"{name} already exists, try another username")
            return redirect(url_for("signup"))
        else:
            all[name] = pw
            update_database(all)
            flash("You have successfully signed up, now try logging in")
            return redirect(url_for("login"))
    return render_template("signup.html", acc_form = form)

@app.route("/login" ,methods = ["Get", "Post"])
def login():
    form = login_form()
    if "name" in session:
        flash("You are already logged in")
        return redirect(url_for("user_dashboard"))
    elif form.validate_on_submit():
        all = open_db()
        name = form.name.data
        pw = form.pw.data
        if name in all:
            if all[name] == pw:
                session.permanent = True
                session["name"] = name
                session["count"] = 0
                flash("Login successful", name)
                return redirect(url_for('user_dashboard'))
        flash("Invalid login! Try again.")
        return redirect(url_for('login'))
    return render_template('login.html', acc_form = form)

@app.route("/user")
def user_dashboard():
    if "name" in session:
        name = session["name"]
        return render_template("dashboard.html", name = name)
    flash("You have not logged in yet")
    return redirect(url_for("login"))

@app.route("/logout", methods=["Get","Post"])
def logout():
    if "name" not in session:
        flash("You have not logged in yet")
        return redirect(url_for("login"))
    name = session["name"]
    db= open_db()
    if "password" in request.form and "name" in session:
        if request.form["password"] == db[name]:
            flash("You have successfully logged out")

            session.pop("name", None)
            session.pop("count", None)
            return redirect("/")
    return render_template("logout.html", name = name)
if __name__ == '__main__':
    app.run(debug=True)
'''

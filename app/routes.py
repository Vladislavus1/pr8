from app import app
from flask import render_template
from app.forms import LoginForm, SignupForm



@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/signup")
def signup():
    form = SignupForm()
    return render_template("signup.html", form=form)

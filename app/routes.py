from app import app
from flask import render_template, request, redirect
from app.forms import LoginForm, SignupForm
from app.database import User, Event, session
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager


def commit_new_item(item):
    session.add(item)
    session.commit()
    session.close()

@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        name = form.nickname.data
        password = form.password.data

        # user = session.query(Student).where(Student.username == username).first()
        user_check = session.query(User).where(User.nickname == name).first()

        if not user_check:
            print(name, password)
            return render_template("main.html", message="Login Error!")

        login_user(user_check)
        return render_template("main.html")

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        name = form.nickname.data
        password = form.password.data
        email = form.email.data
        new_user = User(str(name), str(password), str(email))

        commit_new_item(new_user)
        return render_template("main.html", message="Done!")


    return render_template("signup.html", form=form)

@app.route("/test")
@login_required
def test():
    import requests

    response = requests.get('https://www.boredapi.com/api/activity')
    print(response)
    if response.status_code == 200:
        data = response.json()["activity"]
    else:
        data = "ERROR"

    return render_template("main.html", data=data)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(405)
def handler_error(e):
    return render_template("custom_error.html", error=e.code)

@login_manager.user_loader
def load_user(user):
    return session.query(User).get(int(user))

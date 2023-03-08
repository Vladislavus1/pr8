from app import app
from flask import render_template, request, redirect, make_response, jsonify
from app.forms import LoginForm, SignupForm
from app.database import User, Event, session
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager
from app.db_controls import add_new_item, get_events_by
from datetime import datetime

def convert_time_to_object(time):
    return datetime.strptime(time, "%H:%M").time()

def convert_date_to_object(date):
    return datetime.strptime(date, "%Y-%m-%d").date()

def add_event_to_database(event_data):
    event_data["time"] = convert_time_to_object(event_data["time"])
    event_data["date"] = convert_date_to_object(event_data["date"])
    event_data["user"] = 1
    event = Event(**event_data)
    add_new_item(event)

def commit_new_item(item):
    session.add(item)
    session.commit()
    session.close()

def create_response(status_code):
    response = make_response()
    response.status_code = status_code
    return response

@app.route("/homeworkGet", methods=["GET"])
def func1():
    data = {"arg1": "Pycharm", "arg2": "is cool"}
    response = make_response(jsonify(data))
    return response


@app.route("/homeworkPost", methods=["POST"])
def func2():
    data_from_request = request.get_json()
    print(data_from_request)
    response = make_response()
    response.status_code = 200
    return response


@app.route("/get_events_by_date/<date>", methods=["GET"])
def get_events_by_date(date):
    print(date)
    date = datetime.fromisoformat(date)
    data = get_events_by(date)
    response = make_response(jsonify(data))
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    print(data_from_request)
    try:
        add_event_to_database(data_from_request)
        response = create_response(200)
    except Exception as e:
        print(e)
        response = create_response(500)
    return response

@app.route("/")
@app.route("/main")
def index():
    return "200"

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

# @app.errorhandler(404)
# @app.errorhandler(500)
# @app.errorhandler(405)
# def handler_error(e):
#     return render_template("custom_error.html", error=e.code)

@login_manager.user_loader
def load_user(user):
    return session.query(User).get(int(user))

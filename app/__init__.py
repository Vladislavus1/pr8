from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "SoMeThInG"


from app import routes
import secrets

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app)
JWTManager(app)

from . import routes
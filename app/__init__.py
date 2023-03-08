from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS



app = Flask(__name__)
app.secret_key = "SoMeThInG"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)


from app import routes
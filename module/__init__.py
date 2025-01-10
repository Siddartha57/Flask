from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'bdfc368df5d3fc142b5d53cb'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE']= "filesystem"
app.config['SESSION_USE_SIGNER'] = True
Session(app)
app.app_context().push()
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from module import routes
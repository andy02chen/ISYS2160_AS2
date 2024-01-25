from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

IMAGES_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER
Session(app)
db = SQLAlchemy(app)

from localShop import routes
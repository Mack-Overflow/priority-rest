from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from logger import setup_logger

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Use the appropriate database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger = setup_logger()
db = SQLAlchemy(app)
jwt = JWTManager(app)

from . import routes, models, auth

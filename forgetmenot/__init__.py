from flask import Flask
from models import db
import os

app = Flask(__name__, static_folder='Static')
app.secret_key = 'development key'

import forgetmenot.routes

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB"]
db.init_app(app)


from flask import Flask
from models import db
#import os

app = Flask(__name__)
app.secret_key = 'development key'

import forgetmenot.routes

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://zunayed:password@localhost/forgetmenot"
db.init_app(app)
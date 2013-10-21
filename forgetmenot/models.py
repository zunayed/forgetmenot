from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(100))
    soundcloud_token = db.Column(db.String(100))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email.lower()
        self.setPassword(password)
        self.soundcloud_token = ''
     
    def setPassword(self, password):
        self.pwdhash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.pwdhash, password)


# class Soundcloud(db.Model):
#     uid = db.Column(db.Integer, primary_key = True)

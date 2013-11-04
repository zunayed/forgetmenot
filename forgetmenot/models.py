from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class soundcloud_tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100))
    title = db.Column(db.String(300))
    url = db.Column(db.String(300))
    alive = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('tracks', lazy='dynamic'))

    def __init__(self, artist, title, url, user):
        self.artist = artist
        self.title = title
        self.url = url
        self.user = user
        #set as default
        self.alive = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
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




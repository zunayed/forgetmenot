from forgetmenot import app
from flask import Flask, render_template, request, url_for, redirect, session
from models import db, User
from form import SignupForm, SigninForm

import soundcloud as sc

#create soundcloud client object with app credentials 
client = sc.Client(client_id='4172958b52e31b5f1e0270600d02aa63',
                       client_secret='d1f3656edbd4f2cdf10ced0dce112c4f',
                       redirect_uri='http://localhost:5000/link_services')

@app.route('/')
def home():
	#Look up user in  database using SQLalchemy 
	# user = User.query.filter_by(email = session['email']).first()
	# access_token = client.exchange_token(code = user.soundcloud_token)
	
	# fav = client.get('/me/favorites/', limit = 30)
	# playlist = {}
	# for track in fav:
	# 	playlist[track.user['username']] = track.title

	# return render_template('home.html', data = playlist)
	return "home"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	#intiate for signupForm class from form.py
	form = SignupForm()
	#dive into flask migrations to make sure I don't have to delete tables
	#form validation
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:   
			new_user = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			
			db.session.add(new_user)
			db.session.commit()

			#store in cookies 
			session['email'] = new_user.email
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()


	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signin.html', form=form) 

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('signin'))

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user:
		client = sc.Client(access_token=user.soundcloud_token)
		fav = client.get('/me/favorites/', limit = 30)
		favorites = {}
		for track in fav:
			favorites[track.user['username']] = track.title
		
		return render_template('profile.html', data = favorites)
	else:
		return redirect(url_for('signin'))
	

@app.route('/link_services')
def link_services():
	soundcloud_code = request.args.get('code')

	#*******if soundcloud doesn't come back with show error ******
	access_token = client.exchange_token(code = soundcloud_code) 
	user = User.query.filter_by(email = session['email']).first()
	
	user.soundcloud_token = access_token.access_token
	db.session.commit()

	return redirect(url_for('profile'))

@app.route('/profile/soundcloud')
def soundcloud():
	user = User.query.filter_by(email = session['email']).first()
	#check to see if token already exist in database

	if user.soundcloud_token:	
		return redirect(url_for('profile'))
	else:
		return redirect(client.authorize_url())	

@app.route('/about')
def about():
	return render_template('about.html')

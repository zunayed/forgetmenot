from forgetmenot import app
from flask import Flask, render_template, request, url_for, redirect, session
from dataprep import getSoundcloud 
from models import db, User
from form import SignupForm, SigninForm

import soundcloud

#create soundcloud client object with app credentials
client = soundcloud.Client(client_id='4172958b52e31b5f1e0270600d02aa63',
                       client_secret='d1f3656edbd4f2cdf10ced0dce112c4f',
                       redirect_uri='http://localhost:5000/profile')

@app.route('/')
def home():
	favorites = getData()
	return render_template('home.html', data = favorites)
	#return redirect(url_for('profile'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	db.create_all()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:   
			new_user = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(new_user)
			db.session.commit()

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
	return redirect(url_for('home'))

@app.route('/profile')
def profile():

	soundcloud_token = request.args.get('code', '')
	if soundcloud_token == '':
		print "no token"
	else:
		print "got token"
		client = soundcloud.Client(access_token = soundcloud_token)
		fav = client.get('/me/favorites/', limit = 30)
		playlist = {}
		for track in fav:
			playlist[track.user['username']] = track.title

		print playlist

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')

@app.route('/profile/soundcloud')
def soundcloud():
	return redirect(client.authorize_url())		

@app.route('/about')
def about():
	return render_template('about.html')

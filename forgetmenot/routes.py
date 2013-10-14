from forgetmenot import app
from flask import Flask, render_template, request, url_for, redirect, session
from dataprep import getData 
from models import db, User
from form import SignupForm

@app.route('/')
def home():
	favorites = getData()
	return render_template('home.html', data = favorites)

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

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')

@app.route('/about')
def about():
	return render_template('about.html')

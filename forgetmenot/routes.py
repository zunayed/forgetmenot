from forgetmenot import app
from flask import Flask, render_template, request, url_for, redirect
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
	#student = User.query.filter_by(firstname = 'Zunayed').first()
	#print student
	#print User.query.filter_by(firstname='zunayed').first()
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:   
			student = User(form.firstname.data, form.lastname.data, form.email.data)
			db.session.add(student)
			db.session.commit()
			print student
			return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/about')
def about():
	return render_template('about.html')

from forgetmenot import app
from flask import Flask, render_template, request, url_for, redirect
from dataprep import getData 

@app.route('/')
def home():
	favorites = getData()
	return render_template('home.html', data = favorites)

@app.route('/about')
def about():
	return render_template('about.html')

from flask import Flask, render_template, request, url_for, redirect, session

from forgetmenot import app
from models import db, User, soundcloud_tracks
from form import SignupForm, SigninForm

import soundcloud as sc
import os

# create soundcloud client object with app credentials
client = sc.Client(client_id=os.environ["ID"],
                   client_secret=os.environ["SECRET"],
                   redirect_uri=os.environ["REDIRECT"])


@app.route('/')
def home():
    # db.create_all()
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # intiate for signupForm class from form.py
    form = SignupForm()

    # form validation
    if request.method == 'POST':
        if form.validate() is False:
            # print str(form.errors['email'])
            return render_template('signup.html', form=form)
        else:
            new_user = User(
                form.firstname.data, form.lastname.data, form.email.data, form.password.data)

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
        if form.validate() is False:
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

    user = User.query.filter_by(email=session['email']).first()
    update_track_status(user)

    num_dead = soundcloud_tracks.query.filter_by(alive=False).filter_by(user_id=user.id).count()
    num_alive = soundcloud_tracks.query.filter_by(alive=True).filter_by(user_id=user.id).count()

    if user:
        sc_tracks = soundcloud_tracks.query.filter_by(user_id=user.id).all()
        data = [[item.artist, item.title, item.alive, item.url, item.track_id]
                for item in sc_tracks]

        return render_template(
            'profile.html',
            data=enumerate(data),
            num_alive=num_alive,
            num_dead=num_dead
        )
    else:
        return redirect(url_for('signin'))


def update_track_status(user):
    client = sc.Client(access_token=user.soundcloud_token)
    cloud_fav_list = client.get('/me/favorites/', limit=1000)
    db_tracks = soundcloud_tracks.query.filter_by(user_id=user.id).all()

    # lambda expression vs list comprehension
    # db_data = map(lambda item: item.url, db_tracks)
    db_data = set(item.url for item in db_tracks)
    cloud_url_list = set(track.permalink_url for track in cloud_fav_list)

    for track in db_data - cloud_url_list:
        # track that are not in your soundcloud fav any more and are going to be marked dead
        current_track = soundcloud_tracks.query.filter_by(url=track).first()
        current_track.alive = False

    for track in cloud_url_list - db_data:
        # new tracks to add to database
        trk = [item for item in cloud_fav_list if item.permalink_url == track][0]
        new_track = soundcloud_tracks(
            trk.id,
            trk.user['username'],
            trk.title,
            trk.permalink_url,
            user
        )
        db.session.add(new_track)

    db.session.commit()


@app.route('/link_services')
def link_services():
    if 'code' in request.args:
        soundcloud_code = request.args.get('code')
        access_token = client.exchange_token(code=soundcloud_code)
        user = User.query.filter_by(email=session['email']).first()
        user.soundcloud_token = access_token.access_token
        db.session.commit()

        return redirect(url_for('profile'))

    return redirect(url_for('profile'))


@app.route('/profile/soundcloud')
def soundcloud():
    user = User.query.filter_by(email=session['email']).first()
    # check to see if token already exist in database
    if user.soundcloud_token:
        return redirect(url_for('profile'))
    else:
        return redirect(client.authorize_url())


@app.route('/about')
def about():
    return render_template('about.html')

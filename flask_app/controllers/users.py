from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.workout import Workout
from flask_app.models.exercise import Exercise
from flask import Flask, get_flashed_messages, redirect, session, render_template, request, flash

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html', messages = get_flashed_messages())

@app.route('/register', methods=['post'])
def register():
    if User.is_valid(request.form):
        data = {
            'first_name': request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        session['user_id'] = User.create(data)
        return redirect('/home')
    return redirect('/')

@app.route('/login', methods=['post'])
def login():
    this_user = User.get_by_email({'email': request.form['email']})
    if this_user:
        if bcrypt.check_password_hash(this_user.password, request.form['password']):
            session['user_id'] = this_user.id
            return redirect('/home')
        flash('Incorrect password.')
    else:
        flash('Email does not exist.')
    return redirect('/')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html', user= User.get_by_id({'id': session['user_id']}), users = User.get_all_users(), sightings = Sighting.get_all_sightings())
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')    
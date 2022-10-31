from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.workout import Workout

@app.route('/workouts/new')
def generateWorkout():
    return render_template('newWorkout.html', messages= get_flashed_messages())
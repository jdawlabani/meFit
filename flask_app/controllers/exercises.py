from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.exercise import Exercise

@app.route('/exercises')
def all_Exercises():
    return render_template("allExercises.html", exercises= Exercise.get_all())
@app.route('/exercises/new')
def newExercise():
    return render_template('newExercise.html', messages = get_flashed_messages())

@app.route('/exercises/create', methods=['post'])
def createExercise():
    if Exercise.is_valid(request.form):
        data = {
            'name': request.form['name'],
            'type': request.form['type'],
            'video': request.form['video']
        }
        Exercise.create(data)
        return redirect('/home')
    return redirect('/exercises/new')


from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.exercise import Exercise

@app.route('/exercises')
def all_exercises():
    return render_template("all_exercises.html", exercises= Exercise.get_all())
@app.route('/exercises/new')
def new_exercise():
    return render_template('new_exercise.html', messages = get_flashed_messages())

@app.route('/exercises/create', methods=['post'])
def create_exercise():
    if Exercise.is_valid(request.form):
        data = {
            'name': request.form['name'],
            'type': request.form['type'],
            'video': request.form['video']
        }
        Exercise.create(data)
        return redirect('/home')
    return redirect('/exercises/new')

@app.route('/exercises/edit/<int:id>')
def edit_exercise(id):
    this_exercise = Exercise.get_by_id({'id': id})
    return render_template('edit_exercise.html', exercise = this_exercise, messages = get_flashed_messages)
    


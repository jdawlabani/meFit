from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.workout import Workout

@app.route('/workouts/new')
def new_workout():
    return render_template('new_workout.html', messages= get_flashed_messages())

@app.route('/workouts/create', methods=['post'])
def generate_workout():
    if Workout.is_valid(request.form):
        data = {
            'name': request.form['name'],
            'type': request.form['type'],
            'num_of_exercises': request.form['num_of_exercises'],
            'user_id': session['user_id']
        }
        Workout.create(data)
        return redirect('/home')
    return redirect('/workouts/new')

@app.route('/workouts/edit<int:id>')
def edit_workout(id):
    this_workout = Workout.get_by_id({'id': id})
    return render_template('edit_workout.html', workout = this_workout, messages = get_flashed_messages)

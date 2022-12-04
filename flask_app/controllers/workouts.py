from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.workout import Workout

@app.route('/workouts/new')
def new_workout():
    if 'user_id' in session:
        return render_template('new_workout.html', messages= get_flashed_messages())
    return redirect('/')

@app.route('/workouts/create', methods=['post'])
def generate_workout():
    if 'user_id' in session:
        if Workout.is_valid(request.form):
            data = {
                'name': request.form['name'],
                'type': request.form['type'],
                'num_of_exercises': request.form['num_of_exercises'],
                'user_id': session['user_id']
            }
            id = Workout.create(data)
            data = {
                'name': request.form['name'],
                'type': request.form['type'],
                'num_of_exercises': request.form['num_of_exercises'],
                'user_id': session['user_id'],
                'id': id
            }
            Workout.load_exercises(data)
            return redirect('/home')
        return redirect('/workouts/new')
    return redirect('/')

@app.route('/workouts/<int:id>')
def show_workout(id):
    if 'user_id' in session:
        this_workout = Workout.get_by_id_with_exercises({'id': id, 'user_id': session['user_id']})
        return render_template('show_workout.html', workout = this_workout)
    return redirect('/')

@app.route('/workouts/rate/<int:id>')
def rate_workout(id):
    if 'user_id' in session:
        this_workout = Workout.get_by_id_with_exercises({'id': id, 'user_id': session['user_id']})
        return render_template('rate_workout.html', workout = this_workout)
    return redirect('/')

@app.route('/workouts/confirm_rating/<int:id>', methods = ['post'])
def confirm_workout_rating(id):
    if 'user_id' in session:
        this_workout = Workout.get_by_id_with_exercises({'id': id, 'user_id': session['user_id']})
        data = {
            'rating': request.form['rating'],
            'workout_id': this_workout.id,
            'user_id': session['user_id']
            }
        if this_workout.rating < 0:
            Workout.create_rating(data)
        else:
            Workout.update_rating(data)
        print(this_workout.rating)
        return redirect('/workouts/'+str(id))
    return redirect('/')


@app.route('/workouts/edit/<int:id>')
def edit_workout(id):
    if 'user_id' in session:
        this_workout = Workout.get_by_id({'id': id})
        return render_template('edit_workout.html', workout = this_workout, messages = get_flashed_messages())
    return redirect('/')

@app.route('/workouts/update/<int:id>', methods=['post'])
def update_workout(id):
    if 'user_id' in session:
        if Workout.is_valid(request.form):
            this_workout = Workout.get_by_id({'id': id})
            data = {
                'id': id,
                'name': request.form['name'],
                'type': this_workout.type,
                'user_id': this_workout.user_id,
            }
            Workout.update_by_id(data)
            return redirect('/workouts/'+str(id))
        return redirect('/workouts/edit/'+str(id))
    return redirect('/')

@app.route('/workouts/delete/<int:id>')
def delete_workout(id):
    if 'user_id' in session:
        Workout.delete_by_id({'id': id})
        return redirect('/home')
    return redirect('/')

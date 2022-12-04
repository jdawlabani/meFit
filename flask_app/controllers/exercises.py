from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.exercise import Exercise

@app.route('/exercises')
def all_exercises():
    if 'user_id' in session:
        return render_template("all_exercises.html", exercises= Exercise.get_all_with_ratings({'user_id': session['user_id']}))
    return redirect('/')
@app.route('/exercises/new')
def new_exercise():
    if 'user_id' in session:
        return render_template('new_exercise.html', messages = get_flashed_messages())
    return redirect('/')

@app.route('/exercises/create', methods=['post'])
def create_exercise():
    if 'user_id' in session:
        if Exercise.is_valid(request.form):
            data = {
                'name': request.form['name'],
                'type': request.form['type'],
                'sets': request.form['sets'],
                'reps': request.form['reps'],
                'video': request.form['video']
            }
            Exercise.create(data)
            return redirect('/home')
        return redirect('/exercises/new')
    return redirect('/')

@app.route('/exercises/<int:id>')
def show_exercise(id):
    if 'user_id' in session:
        this_exercise = Exercise.get_by_id_with_rating({'id': id, 'user_id': session['user_id']})
        return render_template('show_exercise.html', exercise = this_exercise)
    return redirect('/')

@app.route('/exercises/rate/<int:id>')
def rate_exercise(id):
    if 'user_id' in session:
        this_exercise = Exercise.get_by_id_with_rating({'id': id, 'user_id': session['user_id']})
        return render_template('rate_exercise.html', exercise = this_exercise)
    return redirect('/')

@app.route('/exercises/confirm_rating/<int:id>', methods = ['post'])
def confirm_exercise_rating(id):
    if 'user_id' in session:
        this_exercise = Exercise.get_by_id_with_rating({'id': id, 'user_id': session['user_id']})
        data = {
            'rating': request.form['rating'],
            'weight': this_exercise.weight,
            'exercise_id': this_exercise.id,
            'user_id': session['user_id']
            }
        if this_exercise.rating < 0:
            Exercise.create_rating(data)
        else:
            Exercise.update_rating(data)
        print(this_exercise.rating)
        return redirect('/exercises/'+str(id))
    return redirect('/')

@app.route('/exercises/edit/<int:id>')
def edit_exercise(id):
    if 'user_id' in session:
        this_exercise = Exercise.get_by_id_with_rating({'id': id, 'user_id': session['user_id']})
        return render_template('edit_exercise.html', exercise = this_exercise, messages = get_flashed_messages())
    return redirect('/')
    
@app.route('/exercises/update/<int:id>', methods=['post'])
def update_exercise(id):
    if 'user_id' in session:
        data = {
            'id' : id,
            'name': request.form['name'],
            'type': request.form['type'],
            'sets': request.form['sets'],
            'reps': request.form['reps'],
            'video': request.form['video']
        }
        if Exercise.is_valid_update(data):
            Exercise.update_by_id(data)
            return redirect('/exercises/'+ str(id))
        return redirect('/exercises/edit/' + str(id))
    return redirect('/')

@app.route('/exercises/delete/<int:id>')
def delete_exercise(id):
    if 'user_id' in session:
        Exercise.delete_by_id({'id': id})
        return redirect('/home')
    return redirect('/')

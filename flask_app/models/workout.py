from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.exercise import Exercise
import random

class Workout:
    db = 'fitness'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        #rating will always be 0 (unrated) on initialization
        self.rating = 0
        self.exercises = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO workouts (name, type, user_id) VALUES (%(name)s, %(type)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def load_exercises(cls, data):
        if data['type'] == 'Full Body':
            exercise_list = Exercise.get_all()
        else:
            exercise_list = Exercise.get_by_type(data)
        workout = Workout.get_by_id(data)
        #if there aren't enough exercises to fill the workout, change the number of exercises
        if len(exercise_list) < int(data['num_of_exercises']):
            data['num_of_exercises'] = len(exercise_list)
        count = 0
        #let's use an array to track what numbers we have already used
        z = []
        while (count < int(data['num_of_exercises'])):
            #choose a random exercise and check if it's already in the workout.
            y = random.randint(0,len(exercise_list)-1)
            if y not in z:
                #grab the id that will go to our many to many table
                ids = {
                    'workout_id': workout.id,
                    'exercise_id': exercise_list[y].id
                }
                #add random number to array to avoid repeats
                z.append(y)
                print(z)
                query = "INSERT INTO workout_exercise (exercise_id, workout_id) VALUES (%(exercise_id)s,%(workout_id)s);"
                connectToMySQL(cls.db).query_db(query, ids)
                #increment count
                count += 1
        return workout

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts;"
        results = connectToMySQL(cls.db).query_db(query)
        workout_list= []
        for dict in results:
            workout_list.append(cls(dict))
        return workout_list

    #needs to be passed in user_id to get ratings from said user
    @classmethod
    def get_all_with_ratings(cls, data):
        query = "SELECT * FROM workouts FULL JOIN workout_rating;"
        results = connectToMySQL(cls.db).query_db(query)
        workout_list= []
        for dict in results:
            if dict['user_id'] == data['user_id'] or not dict['user_id']:
                workout_list.append(cls(dict))
        return workout_list
    @classmethod
    def get_all_with_ratings(cls, data):
        #get all exercises
        query = "SELECT * FROM workouts"
        results = connectToMySQL(cls.db).query_db(query)
        workout_list= []
        rating_list=[]
        for dict in results:
            workout_list.append(cls(dict))
        #get all the ratings for workouts that the user has rated
        query = "SELECT * FROM users LEFT JOIN workout_rating ON workout_rating.user_id = users.id LEFT JOIN workouts ON workout_rating.workout_id = workouts.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        for dict in results:
            temp = {
                'rating': dict['rating'],
                'workout_id': dict['workouts.id']
            }
            rating_list.append(temp)
        for workout in workout_list:
            #start by setting the rating to 0 before checking for user's ratings
            workout.rating = 0
            for rating in rating_list:
                if workout.id == rating['workout_id']:
                    workout.rating = rating['rating']
        return workout_list


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM workouts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_id_with_exercises(cls, data):
        query = "SELECT * FROM workouts LEFT JOIN workout_exercise ON workout_exercise.workout_id = workouts.id LEFT JOIN exercises ON workout_exercise.exercise_id = exercises.id WHERE workouts.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_workout = cls(results[0])
        for dict in results:
            exercise_data = {
                'id': dict['exercises.id'],
                'name': dict['exercises.name'],
                'type': dict['exercises.type'],
                'video': dict['video'],
                'sets': dict['sets'],
                'reps': dict['reps'],
                'created_at': dict['exercises.created_at'],
                'updated_at': dict['exercises.updated_at']
            }
            this_workout.exercises.append(Exercise(exercise_data))
        return this_workout

    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM workouts WHERE name = %(name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_workouts_by_user(cls, data):
        query = "SELECT * FROM workouts WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        workout_list= []
        for dict in results:
            workout_list.append(cls(dict))
        return workout_list

    @classmethod
    def update_by_id(cls, data):
        query = "UPDATE workouts SET name = %(name)s, type = %(type)s, user_id = %(user_id)s WHERE id = %(id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete_by_id(cls, data):
        query = "DELETE FROM workout_exercise WHERE workout_id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def rate(cls, data):
        query = "INSERT INTO workout_rating (user_id, exercise_id, rating) VALUES (%(user_id)s, %(exercise_id)s, %(rating)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_rating(cls, data):
        query = "UPDATE workout_rating SET rating = %(rating)s WHERE id = %(id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @staticmethod
    def is_valid(workout_data):
        is_valid = True
        all_workouts = Workout.get_all()
        if len(workout_data['name']) < 2:
            flash('Workout name must be at least 2 characters long.')
            is_valid = False
        for workout in all_workouts:
            if workout.name == workout_data['name']:
                flash("Workout name must be unique")
                is_valid = False
        return is_valid

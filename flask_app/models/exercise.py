from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

#regex to check URL validation
regex = ("((http|https)://)(www.)?" +
            "[a-zA-Z0-9@:%._\\+~#?&//=]" +
            "{2,256}\\.[a-z]" +
            "{2,6}\\b([-a-zA-Z0-9@:%" +
            "._\\+~#?&//=]*)")

URL_REGEX = re.compile(regex)

class Exercise:
    db = 'fitness'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.video = data['video']
        self.sets = data['sets']
        self.reps = data['reps']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #always start with a 0 (unrated) rating and 0 (unlogged) weight last used when initializing
        self.rating = 0
        self.weight = 0
        self.workouts = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO exercises (name, type, sets, reps, video) VALUES (%(name)s, %(type)s, %(sets)s, %(reps)s, %(video)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM exercises ORDER BY type;"
        results = connectToMySQL(cls.db).query_db(query)
        exercise_list= []
        for dict in results:
            exercise_list.append(cls(dict))
        return exercise_list

    #needs to be passed in user_id to get ratings from said user
    @classmethod
    def get_all_with_ratings(cls, data):
        #get all exercises
        query = "SELECT * FROM exercises"
        results = connectToMySQL(cls.db).query_db(query)
        exercise_list= []
        rating_list=[]
        for dict in results:
            exercise_list.append(cls(dict))
        #get all the ratings for exercises that the user has rated
        query = "SELECT * FROM users LEFT JOIN exercise_rating ON exercise_rating.user_id = users.id LEFT JOIN exercises ON exercise_rating.exercise_id = exercises.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            for dict in results:
                temp = {
                    'rating': dict['rating'],
                    'exercise_id': dict['exercises.id']
                }
                rating_list.append(temp)
        for exercise in exercise_list:
            for rating in rating_list:
                if exercise.id == rating['exercise_id']:
                    exercise.rating = rating['rating']
        return exercise_list

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM exercises WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_id_with_rating(cls, data):
        query = "SELECT * FROM exercises WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_exercise = cls(results[0])
        query = "SELECT * FROM users LEFT JOIN exercise_rating ON exercise_rating.user_id = users.id LEFT JOIN exercises ON exercise_rating.exercise_id = exercises.id WHERE users.id = %(user_id)s AND exercises.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            #results should only have one row if that so access the first row's rating and set it equal to exercise's rating
            this_exercise.rating = results[0]['rating']
        return this_exercise

    @classmethod
    def get_by_type(cls,data):
        query = "SELECT * FROM exercises WHERE type = %(type)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        exercise_list= []
        for dict in results:
            exercise_list.append(cls(dict))
        return exercise_list

    @classmethod
    def update_by_id(cls, data):
        query = "UPDATE exercises SET name = %(name)s, type = %(type)s, sets = %(sets)s, reps = %(reps)s , video = %(video)s WHERE id = %(id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete_by_id(cls, data):
        query = "DELETE FROM workout_exercise WHERE exercise_id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        query = "DELETE FROM exercises WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    @classmethod
    def create_rating(cls, data):
        query = "INSERT INTO exercise_rating (user_id, exercise_id, rating, weight) VALUES (%(user_id)s, %(exercise_id)s, %(rating)s, 0);"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def update_rating(cls, data):
        query = "UPDATE exercise_rating SET rating = %(rating)s WHERE exercise_id = %(exercise_id)s AND user_id = %(user_id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return


    @staticmethod
    def is_valid(exercise_data):
        is_valid = False
        all_exercises = Exercise.get_all()
        all_types = ['Lower Body', 'Push', 'Pull']
        for type in all_types:
            if type == exercise_data['type']:
                is_valid = True
        #if is_valid is still false, then need to flash that the type is invalid
        if not is_valid:
            flash('Invalid type.')
        if len(exercise_data['name']) < 2:
            flash('Exercise name must be at least 2 characters long.')
            is_valid = False
        if not URL_REGEX.match(exercise_data['video']):
            flash('Please enter a valid video URL.')
            is_valid = False
        for exercise in all_exercises:
            if exercise.name == exercise_data['name']:
                flash("Exercise name must be unique")
                is_valid = False
        return is_valid

    #this method is needed for updating because unique check will trip once you check the name against itself in the database if name hasn't been changed
    @staticmethod
    def is_valid_update(exercise_data):
        is_valid = False
        all_exercises = Exercise.get_all()
        all_types = ['Lower Body', 'Push', 'Pull']
        for type in all_types:
            if type == exercise_data['type']:
                is_valid = True
        #if is_valid is still false, then need to flash that the type is invalid
        if not is_valid:
            flash('Invalid type.')
        if len(exercise_data['name']) < 2:
            flash('Exercise name must be at least 2 characters long.')
            is_valid = False
        if not URL_REGEX.match(exercise_data['video']):
            flash('Please enter a valid video URL.')
            is_valid = False
        for exercise in all_exercises:
            if exercise.name == exercise_data['name'] and exercise.id != exercise_data['id']:
                flash("Exercise name must be unique")
                is_valid = False
        return is_valid

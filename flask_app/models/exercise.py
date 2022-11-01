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
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.workouts = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO exercises (name, type, video) VALUES (%(name)s, %(type)s, %(video)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM exercises;"
        results = connectToMySQL(cls.db).query_db(query)
        exercise_list= []
        for dict in results:
            exercise_list.append(cls(dict))
        return exercise_list

    @classmethod
    def update_by_id(cls, data):
        query = "UPDATE exercises SET name = %(name)s, type = %(type)s, video = %(video)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    
    # @classmethod
    # def get_all_exercises_by_workout(cls,data):

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM exercises WHERE id = %(id)s;"
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
        #if is_valid is still false, then the
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

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Workout:
    db = 'meFit'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.exercises = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO workouts (name, user_id) VALUES (%(name)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM workouts;"
        results = connectToMySQL(cls.db).query_db(query)
        workout_list= []
        for dict in results:
            workout_list.append(cls(dict))
        return workout_list

    @classmethod
    def get_all_workouts_by_user(cls, data):
        query = "SELECT * FROM workouts WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query)
        workout_list= []
        for dict in results:
            workout_list.append(cls(dict))
        return workout_list

    @classmethod
    def update_by_id(cls, data):
        query = "UPDATE exercises SET name = %(name)s, type = %(type)s, video = %(video)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    #Still needs completion
    @classmethod
    def get_one_with_exercises(cls, data):
        query = "SELECT * FROM workouts LEFT JOIN "
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @staticmethod
    def is_valid(workout_data):
        is_valid = True
        all_workouts = Workout.get_all()
        if len(workout_data['name']) <= 2:
            flash('Workout name must be at least 2 characters long.')
            is_valid = False
        for workout in all_workouts:
            if workout.name == workout_data['name']:
                flash("Workout name must be unique")
                is_valid = False
        return is_valid

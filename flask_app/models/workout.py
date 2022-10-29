from flask_app.config.mysqlconnection import connectToMySQL


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
    def get_all_workouts_by_user(cls, data):
        query = "SELECT * FROM workouts WHERE user_id = %(user_id)s"


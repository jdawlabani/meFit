from flask_app import app
from flask_app.controllers import users, exercises, workouts

if __name__ == '__main__':
    app.run(debug=True)
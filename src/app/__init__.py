'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Student: Monica Ball
Description: Goal Buddy App
'''

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(Config)
# db initialization - going to migrate to postgreSQL
db = SQLAlchemy(app)
#db.init_app(app)

# login manager
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

with app.app_context():
    db.create_all()

    from app import db
    from app.models import User, Goal
    from werkzeug.security import generate_password_hash
    
    # create test user
    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        test_password = "$Test123"
        test_user = User(
            username = "testuser",
            email = "testuser@example.org",
            name = "Test User",
            password_hash = generate_password_hash(test_password) 
        )

        db.session.add(test_user)
        db.session.commit()

    # create test goal
    test_goal = Goal.query.filter_by(title='My First Goal').first()
    if not test_goal:
        test_goal = Goal(
            title = "My First Goal",
            goal_why = "For testing a Flask app!",
            goal_outcome = "Complete Project 3",
            user_id = 1,
            is_completed = False
        )

        db.session.add(test_goal)
        db.session.commit()

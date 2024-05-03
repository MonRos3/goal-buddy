'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Student: Monica Ball
Description: Goal Buddy App
'''

from flask import Flask
from flask_login import LoginManager
import os
import bcrypt

app = Flask("Goal Buddy Web App")
app.secret_key = 'super-duper top secret key'
app.config['USER SIGN UP'] = 'User Sign Up'
app.config['USER SIGNIN'] = 'User Sign In'

# db initialization - probably going to be cassandra


# import models after initializing db
from app import models

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

# import routes after initializing login_manager
from app import routes
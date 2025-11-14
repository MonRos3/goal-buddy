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
from app.quotes import get_random_quote

@app.context_processor
def inject_quote():
    return {'random_quote': get_random_quote()}

with app.app_context():
    db.create_all()

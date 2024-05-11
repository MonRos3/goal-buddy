'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Student: Monica Ball
Description: Goal Buddy App
'''
from flask_wtf import FlaskForm
from datetime import datetime, date
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms_components import DateField, DateRange
import sqlalchemy as sa
from app import db
from app.models import User, Goal

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class GoalForm(FlaskForm):
    title = StringField('What is your goal?', validators=[DataRequired()], render_kw={"placeholder": "Finish the Deck"})
    goal_why = StringField('Why do you want to achieve this goal?', validators=[DataRequired()], render_kw={"placeholder": "The deck needs refinishing"})
    goal_outcome = StringField('What is your specific measurable outcome?', validators=[DataRequired()], render_kw={"placeholder": "Deck sealant has been applied"})
    goal_due_date = DateField('When do you want to achive this goal?', validators=[DataRequired()])
    submit = SubmitField('Submit')
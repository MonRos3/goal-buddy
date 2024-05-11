'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Student: Monica Ball
Description: Goal Buddy App
'''

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.datastructures import MultiDict

from app import app, db
from app.forms import LoginForm
from app.models import User, Goal
from app.forms import RegistrationForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    next_goal = db.session.scalars(current_user.get_goals().order_by(Goal.goal_due_date.asc())).first()
    in_progress_goals = db.session.scalars(current_user.get_in_progress_goals()).all()
    return render_template('index.html', title='Home', next_goal=next_goal, in_progress_goals=in_progress_goals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect. Sorry.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration finished!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goals = db.session.scalars(current_user.get_goals()).all()
    return render_template('user.html', title='User Goals', user=user, goals=goals)

@app.route('/user/<username>/create_new_goal', methods=['GET', 'POST'])
@login_required
def create_goal(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goals = db.session.scalars(current_user.get_goals()).all()

    form = GoalForm()
    try:
        if form.validate_on_submit():
            new_goal = Goal(
                title=form.title.data,
                goal_why=form.goal_why.data,
                goal_outcome=form.goal_outcome.data,
                user_id=user.id,
                goal_due_date=form.goal_due_date.data
            )
            db.session.add(new_goal)
            db.session.commit()
            return redirect(url_for('index'))
    except Exception as exception:
        flash('Error submitting form')
        print(exception)
    return render_template('create_goal.html', title='Create Goals', user=user, goals=goals, form=form)
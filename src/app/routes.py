'''
Routes; includes user authentication, goal and milestone management.
'''

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.datastructures import MultiDict

from app import app, db
from app.forms import LoginForm, GoalForm, MilestoneForm
from app.models import User, Goal, Milestone
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

    goals_with_milestones = []
    for goal in goals:
        milestones = db.session.scalars(sa.select(Milestone).where(Milestone.goal_id == goal.id).order_by(Milestone.milestone_due_date.asc())).all()
        goals_with_milestones.append({'goal': goal, 'milestones': milestones})

    return render_template('user.html', title='User Goals', user=user, goals_with_milestones=goals_with_milestones)

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
                goal_due_date=form.goal_due_date.data,
                is_date_locked=form.is_date_locked.data
            )
            db.session.add(new_goal)
            db.session.commit()
            return redirect(url_for('index'))
    except Exception as exception:
        flash('Error submitting form')
        print(exception)
    return render_template('create_goal.html', title='Create Goals', user=user, goals=goals, form=form)

@app.route('/user/<username>/goal/<int:goal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_goal(username, goal_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))

    form = GoalForm()
    try:
        if form.validate_on_submit():
            goal.title = form.title.data
            goal.goal_why = form.goal_why.data
            goal.goal_outcome = form.goal_outcome.data
            if not goal.is_date_locked:
                goal.goal_due_date = form.goal_due_date.data
            goal.is_date_locked = form.is_date_locked.data
            db.session.commit()
            flash('Goal updated successfully!')
            return redirect(url_for('user', username=username))
    except Exception as exception:
        flash('Error updating goal')
        print(exception)

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}')

    form.title.data = goal.title
    form.goal_why.data = goal.goal_why
    form.goal_outcome.data = goal.goal_outcome
    form.goal_due_date.data = goal.goal_due_date
    form.is_date_locked.data = goal.is_date_locked

    return render_template('edit_goal.html', title='Edit Goal', user=user, goal=goal, form=form)

@app.route('/user/<username>/goal/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(username, goal_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))

    try:
        db.session.delete(goal)
        db.session.commit()
        flash('Goal deleted successfully!')
    except Exception as exception:
        flash('Error deleting goal')
        print(exception)

    return redirect(url_for('user', username=username))

@app.route('/user/<username>/goal/<int:goal_id>/toggle_complete', methods=['POST'])
@login_required
def toggle_complete_goal(username, goal_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))

    try:
        goal.is_completed = not goal.is_completed
        db.session.commit()
        status = 'completed' if goal.is_completed else 'reopened'
        flash(f'Goal {status} successfully!')
    except Exception as exception:
        flash('Error updating goal status')
        print(exception)

    return redirect(url_for('user', username=username))

@app.route('/user/<username>/goal/<int:goal_id>/milestone/create', methods=['GET', 'POST'])
@login_required
def create_milestone(username, goal_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))

    form = MilestoneForm()
    try:
        if form.validate_on_submit():
            new_milestone = Milestone(
                milestone_title=form.milestone_title.data,
                milestone_due_date=form.milestone_due_date.data,
                milestone_reward=form.milestone_reward.data,
                goal_id=goal.id
            )
            db.session.add(new_milestone)
            db.session.commit()
            flash('Milestone created successfully!')
            return redirect(url_for('user', username=username))
    except Exception as exception:
        flash('Error creating milestone')
        print(exception)

    return render_template('create_milestone.html', title='Create Milestone', user=user, goal=goal, form=form)

@app.route('/user/<username>/goal/<int:goal_id>/milestone/<int:milestone_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_milestone(username, goal_id, milestone_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))
    milestone = db.first_or_404(sa.select(Milestone).where(sa.and_(Milestone.id == milestone_id, Milestone.goal_id == goal.id)))

    form = MilestoneForm()
    try:
        if form.validate_on_submit():
            milestone.milestone_title = form.milestone_title.data
            milestone.milestone_due_date = form.milestone_due_date.data
            milestone.milestone_reward = form.milestone_reward.data
            db.session.commit()
            flash('Milestone updated successfully!')
            return redirect(url_for('user', username=username))
    except Exception as exception:
        flash('Error updating milestone')
        print(exception)

    form.milestone_title.data = milestone.milestone_title
    form.milestone_due_date.data = milestone.milestone_due_date
    form.milestone_reward.data = milestone.milestone_reward

    return render_template('edit_milestone.html', title='Edit Milestone', user=user, goal=goal, milestone=milestone, form=form)

@app.route('/user/<username>/goal/<int:goal_id>/milestone/<int:milestone_id>/delete', methods=['POST'])
@login_required
def delete_milestone(username, goal_id, milestone_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))
    milestone = db.first_or_404(sa.select(Milestone).where(sa.and_(Milestone.id == milestone_id, Milestone.goal_id == goal.id)))

    try:
        db.session.delete(milestone)
        db.session.commit()
        flash('Milestone deleted successfully!')
    except Exception as exception:
        flash('Error deleting milestone')
        print(exception)

    return redirect(url_for('user', username=username))

@app.route('/user/<username>/goal/<int:goal_id>/milestone/<int:milestone_id>/toggle_complete', methods=['POST'])
@login_required
def toggle_complete_milestone(username, goal_id, milestone_id):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    goal = db.first_or_404(sa.select(Goal).where(sa.and_(Goal.id == goal_id, Goal.user_id == user.id)))
    milestone = db.first_or_404(sa.select(Milestone).where(sa.and_(Milestone.id == milestone_id, Milestone.goal_id == goal.id)))

    try:
        milestone.milestone_status = not milestone.milestone_status
        db.session.commit()
        status = 'completed' if milestone.milestone_status else 'reopened'
        flash(f'Milestone {status} successfully!')
    except Exception as exception:
        flash('Error updating milestone status')
        print(exception)

    return redirect(url_for('user', username=username))
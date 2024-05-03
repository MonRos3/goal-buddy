'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Student: Monica Ball
Description: Goal Buddy App
'''

from app import app, db, load_user
from app.models import User, Order, Product, Customer, Administrator, Item
from app.forms import SignUpForm, LoginForm, OrderForm, ProductForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime, timezone
import bcrypt
            
@app.route('/')
@app.route('/index')
@app.route('/index.html')

def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data == form.passwd_confirm.data:
            hashed_password = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(id=form.id.data, name=form.name.data, passwd=hashed_password)
            db.session.add(new_user)
            try:
                db.session.commit()
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash('ID already exists or error in database operation', 'error')
        else:
            flash('Passwords do not match', 'error')
    return render_template('signup.html', form=form)

    
@app.route('/users/login', methods=['GET', 'POST'])
def login():

    adminUser = User.query.filter_by(id='tmota').first()
    admin_id = adminUser.id

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            if user.id in admin_id:  # check if user ID is in admin_id list

                # print(adminUser.creation_date)

                return redirect(url_for('admin'))  # redirect admin to admin page
            else:
                return redirect(url_for('index'))  # redirect regular user to index page
        else:
            return redirect(url_for('login_failed'))  # incorrect credentials
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

# function to handle login/signup failed
@app.route('/users/login_failed')
def login_failed():
    return render_template('login_failed.html')
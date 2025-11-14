'''
test_forms.py
Description: Unit tests for all forms with validation testing
'''

import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from datetime import date, timedelta
from app import app, db
from app.models import User, Goal
from app.forms import LoginForm, RegistrationForm, GoalForm, MilestoneForm, EmptyForm

class LoginFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_form_validation(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'testpass'})
        self.assertTrue(form.validate())

    def test_login_form_missing_username(self):
        form = LoginForm(data={'username': '', 'password': 'testpass'})
        self.assertFalse(form.validate())

    def test_login_form_missing_password(self):
        form = LoginForm(data={'username': 'testuser', 'password': ''})
        self.assertFalse(form.validate())


class RegistrationFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_form_validation(self):
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertTrue(form.validate())

    def test_registration_form_password_mismatch(self):
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertFalse(form.validate())

    def test_registration_form_invalid_email(self):
        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'notanemail',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())

    def test_registration_form_duplicate_username(self):
        u = User(username='existinguser', email='existing@example.com', name='Existing User')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        form = RegistrationForm(data={
            'username': 'existinguser',
            'email': 'new@example.com',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())

    def test_registration_form_duplicate_email(self):
        u = User(username='existinguser', email='existing@example.com', name='Existing User')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        form = RegistrationForm(data={
            'username': 'newuser',
            'email': 'existing@example.com',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())


class GoalFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_goal_form_validation(self):
        future_date = date.today() + timedelta(days=30)
        form = GoalForm(data={
            'title': 'Test Goal',
            'goal_why': 'Test Why',
            'goal_outcome': 'Test Outcome',
            'goal_due_date': future_date,
            'is_date_locked': False
        })
        self.assertTrue(form.validate())

    def test_goal_form_missing_title(self):
        future_date = date.today() + timedelta(days=30)
        form = GoalForm(data={
            'title': '',
            'goal_why': 'Test Why',
            'goal_outcome': 'Test Outcome',
            'goal_due_date': future_date,
            'is_date_locked': False
        })
        self.assertFalse(form.validate())

    def test_goal_form_missing_why(self):
        future_date = date.today() + timedelta(days=30)
        form = GoalForm(data={
            'title': 'Test Goal',
            'goal_why': '',
            'goal_outcome': 'Test Outcome',
            'goal_due_date': future_date,
            'is_date_locked': False
        })
        self.assertFalse(form.validate())

    def test_goal_form_missing_outcome(self):
        future_date = date.today() + timedelta(days=30)
        form = GoalForm(data={
            'title': 'Test Goal',
            'goal_why': 'Test Why',
            'goal_outcome': '',
            'goal_due_date': future_date,
            'is_date_locked': False
        })
        self.assertFalse(form.validate())

    def test_goal_form_with_date_locked(self):
        future_date = date.today() + timedelta(days=30)
        form = GoalForm(data={
            'title': 'Test Goal',
            'goal_why': 'Test Why',
            'goal_outcome': 'Test Outcome',
            'goal_due_date': future_date,
            'is_date_locked': True
        })
        self.assertTrue(form.validate())


class MilestoneFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_milestone_form_validation(self):
        future_date = date.today() + timedelta(days=7)
        form = MilestoneForm(data={
            'milestone_title': 'Test Milestone',
            'milestone_due_date': future_date,
            'milestone_reward': 'Ice cream'
        })
        self.assertTrue(form.validate())

    def test_milestone_form_missing_title(self):
        future_date = date.today() + timedelta(days=7)
        form = MilestoneForm(data={
            'milestone_title': '',
            'milestone_due_date': future_date,
            'milestone_reward': 'Ice cream'
        })
        self.assertFalse(form.validate())

    def test_milestone_form_missing_reward(self):
        future_date = date.today() + timedelta(days=7)
        form = MilestoneForm(data={
            'milestone_title': 'Test Milestone',
            'milestone_due_date': future_date,
            'milestone_reward': ''
        })
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()

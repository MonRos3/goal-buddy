'''
test_routes.py
Description: Integration tests for authentication and goal CRUD routes
'''

import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from datetime import date, timedelta
from app import app, db
from app.models import User, Goal, Milestone

class AuthenticationRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_registration_flow(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'name': 'New User',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        user = db.session.query(User).filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')

    def test_login_flow(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index_requires_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_index_after_login(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class GoalCRUDRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='testuser', email='test@example.com', name='Test User')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_goal(self):
        future_date = date.today() + timedelta(days=30)
        response = self.client.post(f'/user/{self.user.username}/create_new_goal', data={
            'title': 'New Goal',
            'goal_why': 'Because I want to',
            'goal_outcome': 'Complete the task',
            'goal_due_date': future_date,
            'is_date_locked': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        goal = db.session.query(Goal).filter_by(title='New Goal').first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.goal_why, 'Because I want to')

    def test_user_goals_page(self):
        response = self.client.get(f'/user/{self.user.username}')
        self.assertEqual(response.status_code, 200)

    def test_edit_goal(self):
        goal = Goal(title='Original Title', goal_why='Original Why', goal_outcome='Original Outcome', user_id=self.user.id)
        db.session.add(goal)
        db.session.commit()

        future_date = date.today() + timedelta(days=30)
        response = self.client.post(f'/user/{self.user.username}/goal/{goal.id}/edit', data={
            'title': 'Updated Title',
            'goal_why': 'Updated Why',
            'goal_outcome': 'Updated Outcome',
            'goal_due_date': future_date,
            'is_date_locked': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        updated_goal = db.session.query(Goal).filter_by(id=goal.id).first()
        self.assertEqual(updated_goal.title, 'Updated Title')

    def test_delete_goal(self):
        goal = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=self.user.id)
        db.session.add(goal)
        db.session.commit()
        goal_id = goal.id

        response = self.client.post(f'/user/{self.user.username}/goal/{goal_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        deleted_goal = db.session.query(Goal).filter_by(id=goal_id).first()
        self.assertIsNone(deleted_goal)

    def test_toggle_complete_goal(self):
        goal = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=self.user.id, is_completed=False)
        db.session.add(goal)
        db.session.commit()

        response = self.client.post(f'/user/{self.user.username}/goal/{goal.id}/toggle_complete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        updated_goal = db.session.query(Goal).filter_by(id=goal.id).first()
        self.assertTrue(updated_goal.is_completed)


class MilestoneCRUDRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='testuser', email='test@example.com', name='Test User')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

        self.goal = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=self.user.id)
        db.session.add(self.goal)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_milestone(self):
        future_date = date.today() + timedelta(days=7)
        response = self.client.post(f'/user/{self.user.username}/goal/{self.goal.id}/milestone/create', data={
            'milestone_title': 'Test Milestone',
            'milestone_due_date': future_date,
            'milestone_reward': 'Ice cream'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        milestone = db.session.query(Milestone).filter_by(milestone_title='Test Milestone').first()
        self.assertIsNotNone(milestone)
        self.assertEqual(milestone.milestone_reward, 'Ice cream')

    def test_edit_milestone(self):
        milestone = Milestone(milestone_title='Original Title', milestone_reward='Original Reward', goal_id=self.goal.id)
        db.session.add(milestone)
        db.session.commit()

        future_date = date.today() + timedelta(days=7)
        response = self.client.post(f'/user/{self.user.username}/goal/{self.goal.id}/milestone/{milestone.id}/edit', data={
            'milestone_title': 'Updated Title',
            'milestone_due_date': future_date,
            'milestone_reward': 'Updated Reward'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        updated_milestone = db.session.query(Milestone).filter_by(id=milestone.id).first()
        self.assertEqual(updated_milestone.milestone_title, 'Updated Title')

    def test_delete_milestone(self):
        milestone = Milestone(milestone_title='Test Milestone', milestone_reward='Test Reward', goal_id=self.goal.id)
        db.session.add(milestone)
        db.session.commit()
        milestone_id = milestone.id

        response = self.client.post(f'/user/{self.user.username}/goal/{self.goal.id}/milestone/{milestone_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        deleted_milestone = db.session.query(Milestone).filter_by(id=milestone_id).first()
        self.assertIsNone(deleted_milestone)

    def test_toggle_complete_milestone(self):
        milestone = Milestone(milestone_title='Test Milestone', milestone_reward='Test Reward', goal_id=self.goal.id, milestone_status=False)
        db.session.add(milestone)
        db.session.commit()

        response = self.client.post(f'/user/{self.user.username}/goal/{self.goal.id}/milestone/{milestone.id}/toggle_complete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        updated_milestone = db.session.query(Milestone).filter_by(id=milestone.id).first()
        self.assertTrue(updated_milestone.milestone_status)


class QuoteContextProcessorTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_random_quote_in_context(self):
        with app.test_request_context():
            from app import inject_quote
            context = inject_quote()
            self.assertIn('random_quote', context)
            self.assertIsInstance(context['random_quote'], str)


class IndexRouteTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='testuser', email='test@example.com', name='Test User')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_with_no_goals(self):
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_with_goals(self):
        goal = Goal(title='Test Goal', goal_why='Why', goal_outcome='Outcome', user_id=self.user.id)
        db.session.add(goal)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)


class ErrorHandlingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='testuser', email='test@example.com', name='Test User')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_edit_goal_not_found(self):
        response = self.client.get(f'/user/{self.user.username}/goal/999/edit')
        self.assertEqual(response.status_code, 404)

    def test_delete_goal_not_found(self):
        response = self.client.post(f'/user/{self.user.username}/goal/999/delete')
        self.assertEqual(response.status_code, 404)

    def test_create_milestone_goal_not_found(self):
        response = self.client.get(f'/user/{self.user.username}/goal/999/milestone/create')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

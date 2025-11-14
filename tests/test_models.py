'''
test_models.py
Description: Unit tests for User, Goal, and Milestone models
'''

import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from datetime import date, timedelta
from app import app, db
from app.models import User, Goal, Milestone

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        self.assertFalse(u.check_password('wrongpassword'))
        self.assertTrue(u.check_password('testpassword'))

    def test_user_creation(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()
        self.assertIsNotNone(u.id)
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.email, 'test@example.com')
        self.assertEqual(u.name, 'Test User')

    def test_user_repr(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        self.assertEqual(repr(u), '<User testuser>')

    def test_get_goals(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g1 = Goal(title='Goal 1', goal_why='Why 1', goal_outcome='Outcome 1', user_id=u.id)
        g2 = Goal(title='Goal 2', goal_why='Why 2', goal_outcome='Outcome 2', user_id=u.id)
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()

        goals = db.session.scalars(u.get_goals()).all()
        self.assertEqual(len(goals), 2)

    def test_get_completed_goals(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g1 = Goal(title='Goal 1', goal_why='Why 1', goal_outcome='Outcome 1', user_id=u.id, is_completed=True)
        g2 = Goal(title='Goal 2', goal_why='Why 2', goal_outcome='Outcome 2', user_id=u.id, is_completed=False)
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()

        completed_goals = db.session.scalars(u.get_completed_goals()).all()
        self.assertEqual(len(completed_goals), 1)
        self.assertEqual(completed_goals[0].title, 'Goal 1')

    def test_get_in_progress_goals(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g1 = Goal(title='Goal 1', goal_why='Why 1', goal_outcome='Outcome 1', user_id=u.id, is_completed=True)
        g2 = Goal(title='Goal 2', goal_why='Why 2', goal_outcome='Outcome 2', user_id=u.id, is_completed=False)
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()

        in_progress_goals = db.session.scalars(u.get_in_progress_goals()).all()
        self.assertEqual(len(in_progress_goals), 1)
        self.assertEqual(in_progress_goals[0].title, 'Goal 2')


class GoalModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_goal_creation(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id)
        db.session.add(g)
        db.session.commit()

        self.assertIsNotNone(g.id)
        self.assertEqual(g.title, 'Test Goal')
        self.assertEqual(g.goal_why, 'Test Why')
        self.assertEqual(g.goal_outcome, 'Test Outcome')
        self.assertEqual(g.is_completed, False)
        self.assertEqual(g.is_date_locked, False)

    def test_goal_default_due_date(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id)
        db.session.add(g)
        db.session.commit()

        expected_date = date.today() + timedelta(days=7)
        self.assertEqual(g.goal_due_date, expected_date)

    def test_goal_repr(self):
        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=1)
        self.assertEqual(repr(g), '<Goal Test Goal>')

    def test_complete_goal(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id)
        db.session.add(g)
        db.session.commit()

        self.assertFalse(g.is_completed)
        g.complete_goal()
        self.assertTrue(g.is_completed)

    def test_goal_date_lock(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id, is_date_locked=True)
        db.session.add(g)
        db.session.commit()

        self.assertTrue(g.is_date_locked)


class MilestoneModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_milestone_creation(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id)
        db.session.add(g)
        db.session.commit()

        m = Milestone(milestone_title='Test Milestone', milestone_reward='Ice cream', goal_id=g.id)
        db.session.add(m)
        db.session.commit()

        self.assertIsNotNone(m.id)
        self.assertEqual(m.milestone_title, 'Test Milestone')
        self.assertEqual(m.milestone_reward, 'Ice cream')
        self.assertEqual(m.milestone_status, False)
        self.assertEqual(m.goal_id, g.id)

    def test_milestone_default_due_date(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id)
        db.session.add(g)
        db.session.commit()

        m = Milestone(milestone_title='Test Milestone', milestone_reward='Ice cream', goal_id=g.id)
        db.session.add(m)
        db.session.commit()

        expected_date = date.today() + timedelta(days=3)
        self.assertEqual(m.milestone_due_date, expected_date)

    def test_milestone_repr(self):
        m = Milestone(milestone_title='Test Milestone', milestone_reward='Ice cream', goal_id=1)
        self.assertEqual(repr(m), '<Milestone Test Milestone>')

    def test_milestone_relationship_with_goal(self):
        u = User(username='testuser', email='test@example.com', name='Test User')
        u.set_password('testpassword')
        db.session.add(u)
        db.session.commit()

        g = Goal(title='Test Goal', goal_why='Test Why', goal_outcome='Test Outcome', user_id=u.id)
        db.session.add(g)
        db.session.commit()

        m1 = Milestone(milestone_title='Milestone 1', milestone_reward='Reward 1', goal_id=g.id)
        m2 = Milestone(milestone_title='Milestone 2', milestone_reward='Reward 2', goal_id=g.id)
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()

        import sqlalchemy as sa
        milestones = db.session.scalars(sa.select(Milestone).where(Milestone.goal_id == g.id)).all()
        self.assertEqual(len(milestones), 2)


if __name__ == '__main__':
    unittest.main()

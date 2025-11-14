'''
Database models for the Goal Buddy App.
'''

from datetime import datetime, timezone, timedelta, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # field to link goals to user
    goals: so.WriteOnlyMapped['Goal'] = so.relationship(back_populates='goal_owner')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    def get_goals(self):
        print(self.id)
        return sa.select(Goal).where(Goal.user_id == self.id)
    
    def get_completed_goals(self):
        return sa.select(Goal).where(sa.and_(Goal.user_id == self.id, Goal.is_completed == True))
    
    def get_in_progress_goals(self):
        return sa.select(Goal).where(sa.and_(Goal.user_id == self.id, Goal.is_completed == False)).order_by(Goal.timestamp.desc())

class Goal(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    goal_why: so.Mapped[str] = so.mapped_column(sa.String(256))
    goal_outcome: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    goal_due_date: so.Mapped[date] = so.mapped_column(index=True, default=date.today() + timedelta(days=7))
    is_date_locked: so.Mapped[bool] = so.mapped_column(default=False)
    is_completed: so.Mapped[bool] = so.mapped_column(default=False)
    goal_owner: so.Mapped[User] = so.relationship(back_populates='goals')
    milestones: so.WriteOnlyMapped['Milestone'] = so.relationship(back_populates='milestone_goal', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return '<Goal {}>'.format(self.title)

    def complete_goal(self):
        self.is_completed = True

class Milestone(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    milestone_title: so.Mapped[str] = so.mapped_column(sa.String(256))
    milestone_due_date: so.Mapped[date] = so.mapped_column(index=True, default=date.today() + timedelta(days=3))
    milestone_reward: so.Mapped[str] = so.mapped_column(sa.String(256))
    milestone_status: so.Mapped[bool] = so.mapped_column(default=False)
    goal_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Goal.id, ondelete='CASCADE'), index=True)
    milestone_goal: so.Mapped[Goal] = so.relationship(back_populates='milestones')

    def __repr__(self):
        return '<Milestone {}>'.format(self.milestone_title)
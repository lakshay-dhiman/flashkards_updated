from os import name
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from requests import models
from .database import db
from flask_security import  UserMixin, RoleMixin
from sqlalchemy.sql import func

roles_users = db.Table('roles_users',
    db.Column('user_id',db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id',db.Integer,db.ForeignKey('roles.id'))
)

class Roles(db.Model,RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String(255))


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(30), unique=True, nullable = False)
    password = db.Column(db.String(300), nullable=False)
    revised = db.Column(db.Boolean(), default = False)
    revised_month = db.Column(db.Integer(), default = 0)
    decks_created_month = db.Column(db.Integer(), default = 0)
    cards_created_month = db.Column(db.Integer(), default = 0)
    visited_month = db.Column(db.Integer(), default = 0)
    udeck = db.relationship('Decks', cascade='all, delete-orphan', backref='deck')
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Roles',secondary=roles_users,backref=db.backref('users',lazy='dynamic'))


class Decks(db.Model):
    __tablename__ = 'decks'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique=True, nullable = False)
    user_id = db.Column(db.Integer,  db.ForeignKey('users.id'))
    last_rev = db.Column(db.DateTime(timezone=True), default=func.now())
    count = db.Column(db.Integer, default = 0)
    score = db.Column(db.Integer, default= 0)
    dcard = db.relationship('Cards', cascade='all, delete-orphan', backref='card')

class Cards(db.Model):
    __tablename__ = 'cards'
    front = db.Column(db.String(30))
    back = db.Column(db.String(30))
    id = db.Column(db.Integer, primary_key = True)
    deck_id = db.Column(db.Integer,  db.ForeignKey('decks.id'))

# class Score(db.Model):
#     __tablename__ = 'score'
#     score = db.Column(db.Integer, default= 0)
#     deck_id = db.Column(db.Integer,  db.ForeignKey('decks.id'), primary_key = True)
#     count = db.Column(db.Integer, default = 0)
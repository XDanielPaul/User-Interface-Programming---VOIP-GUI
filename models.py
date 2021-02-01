from flask_login import UserMixin
from extensions import db
import pandas as pd


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    image_path = db.Column(db.String(60))
    notifications = db.relationship('Notification', backref='user')
    contacts = db.relationship('Contact', backref='user')


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    image_path = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notifications = db.relationship('Notification', backref='contact')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer)
    timestamp = db.Column(db.String(14))
    confirmed = db.Column(db.Integer)
    time_created = db.Column(db.String(10))
    date_created = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True, nullable=False)
    email = db.Column(db.String(1600), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    notes = db.relationship('Notes', backref='user')

    def __repr__(self):
        return f'email>> {self.email}'


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(100000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Notes_id>> {self.id}'

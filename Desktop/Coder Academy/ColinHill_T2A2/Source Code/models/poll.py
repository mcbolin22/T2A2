# Import necessary modules and functions
from datetime import datetime
from marshmallow import fields, validates, Schema
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from init import db, ma

# Define the Poll model that represents the 'polls' table in the database
class Poll(db.Model):
    __tablename__ = "polls"  # The table name in the database is 'polls'

    # Define the columns in the 'polls' table
    id = db.Column(db.Integer, primary_key=True)  # 'id' is the primary key
    title = db.Column(db.String(100), nullable=False)  # 'title' is a string column that cannot be null
    description = db.Column(db.Text)  # 'description' is a text column
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 'created_at' is a datetime column with a default value of the current time

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 'user_id' is a foreign key that references the 'id' column in the 'users' table

    # Define the relationships with the 'users', 'options', and 'votes' tables
    user = db.relationship("User", back_populates="polls")  # A poll is associated with one user
    options = db.relationship("Option", back_populates="poll")  # A poll can have many options
    votes = db.relationship('Vote', back_populates='poll', lazy=True)  # A poll can have many votes


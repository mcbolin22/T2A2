# Import necessary modules and functions
from init import db, ma
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# Define the Vote model that represents the 'votes' table in the database
class Vote(db.Model):
    __tablename__ = "votes"  # The table name in the database is 'votes'

    # Define the columns in the 'votes' table
    id = db.Column(db.Integer, primary_key=True)  # 'id' is the primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 'user_id' is a foreign key that references the 'id' column in the 'users' table
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=False)  # 'option_id' is a foreign key that references the 'id' column in the 'options' table
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)  # 'poll_id' is a foreign key that references the 'id' column in the 'polls' table

    # Define the relationships with the 'users', 'options', and 'polls' tables
    user = db.relationship('User', back_populates='votes')  # A vote is associated with one user
    option = db.relationship('Option', back_populates='votes')  # A vote is associated with one option
    poll = db.relationship('Poll', back_populates='votes')  # A vote is associated with one poll

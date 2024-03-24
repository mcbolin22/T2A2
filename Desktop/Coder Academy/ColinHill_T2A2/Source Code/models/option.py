# Import necessary modules and functions
from init import db, ma
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# Define the Option model that represents the 'options' table in the database
class Option(db.Model):
    __tablename__ = "options"  # The table name in the database is 'options'

    # Define the columns in the 'options' table
    id = db.Column(db.Integer, primary_key=True)  # 'id' is the primary key
    text = db.Column(db.String, nullable=False)  # 'text' is a string column that cannot be null
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))  # 'poll_id' is a foreign key that references the 'id' column in the 'polls' table

    # Define the relationships with the 'polls' and 'votes' tables
    poll = db.relationship('Poll', back_populates='options')  # An option is associated with one poll
    votes = db.relationship('Vote', back_populates='option')  # An option can have many votes

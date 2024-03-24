# Import necessary modules and functions
from init import db, ma
from .schemas import UserSchema
from marshmallow import fields, Schema, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# Define the User model that represents the 'users' table in the database
class User(db.Model):
    __tablename__ = 'users'  # The table name in the database is 'users'
    __table_args__ = {'extend_existing': True}  # This allows altering the table definition without dropping the existing table

    # Define the columns in the 'users' table
    id = db.Column(db.Integer, primary_key=True)  # 'id' is the primary key
    name = db.Column(db.String)  # 'name' is a string column
    email = db.Column(db.String, nullable=False, unique=True)  # 'email' is a unique string column that cannot be null
    password = db.Column(db.String(128), nullable=True)  # 'password' is a string column that can be null
    is_admin = db.Column(db.Boolean, default=False)  # 'is_admin' is a boolean column with a default value of False

    # Define the relationships with the 'polls' and 'votes' tables
    polls = db.relationship('Poll', backref='user', lazy=True)  # A user can have many polls
    votes = db.relationship('Vote', back_populates='user')  # A user can have many votes

user_schema = UserSchema()  # Create an instance of the UserSchema class
users_schema = UserSchema(many=True)  # Create an instance of the UserSchema class for multiple users


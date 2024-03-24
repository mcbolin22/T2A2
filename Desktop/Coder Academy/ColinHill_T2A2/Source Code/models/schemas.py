from init import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import post_load, validate
from models import User, Poll, Vote, Option  # import your models here

# UserSchema represents the User table in the database
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User  # The User model is used as the base
        include_relationships = True  # Include relationships in the schema
        load_instance = True  # Allow loading instances of User

    # Each auto_field represents a column in the User table
    id = auto_field()
    name = auto_field(validate=validate.Length(min=1, max=100))
    email = auto_field(validate=validate.Email())
    is_admin = auto_field()
    # Nested fields represent relationships with other tables
    # 'polls' represents the one-to-many relationship between User and Poll
    # 'votes' represents the one-to-many relationship between User and Vote
    polls = Nested('PollSchema', many=True, exclude=('user',))
    votes = Nested('VoteSchema', many=True, exclude=('user',))

# PollSchema represents the Poll table in the database
class PollSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Poll  # The Poll model is used as the base
        include_relationships = True  # Include relationships in the schema
        load_instance = True  # Allow loading instances of Poll

    # Each auto_field represents a column in the Poll table
    id = auto_field()
    title = auto_field(validate=validate.Length(min=1, max=200))
    description = auto_field(validate=validate.Length(max=500))
    created_at = auto_field()
    user_id = auto_field()
    # Nested fields represent relationships with other tables
    # 'user' represents the many-to-one relationship between Poll and User
    # 'options' represents the one-to-many relationship between Poll and Option
    # 'votes' represents the one-to-many relationship between Poll and Vote
    user = Nested('UserSchema', exclude=('polls', 'votes'))
    options = Nested('OptionSchema', many=True)
    votes = Nested('VoteSchema', many=True, exclude=('poll',))

# VoteSchema represents the Vote table in the database
class VoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vote  # The Vote model is used as the base
        include_relationships = True  # Include relationships in the schema
        load_instance = True  # Allow loading instances of Vote

    # Each auto_field represents a column in the Vote table
    id = auto_field(dump_only=True)
    user_id = auto_field()
    option_id = auto_field()
    poll_id = auto_field()
    # Nested fields represent relationships with other tables
    # 'user' represents the many-to-one relationship between Vote and User
    # 'option' represents the many-to-one relationship between Vote and Option
    # 'poll' represents the many-to-one relationship between Vote and Poll
    user = Nested('UserSchema', exclude=('votes',))
    option = Nested('OptionSchema', exclude=('votes',))
    poll = Nested('PollSchema', exclude=('votes',))

# OptionSchema represents the Option table in the database
class OptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Option  # The Option model is used as the base
        include_relationships = True  # Include relationships in the schema
        load_instance = True  # Allow loading instances of Option

    # Each auto_field represents a column in the Option table
    id = auto_field()
    text = auto_field(validate=validate.Length(min=1, max=200))
    poll_id = auto_field()
    # Nested fields represent relationships with other tables
    # 'poll' represents the many-to-one relationship between Option and Poll
    # 'votes' represents the one-to-many relationship between Option and Vote
    poll = Nested('PollSchema', exclude=('options',))
    votes = Nested('VoteSchema', many=True, exclude=('option',))
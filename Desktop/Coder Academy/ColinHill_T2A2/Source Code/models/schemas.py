from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from models import User, Poll, Vote, Option  # import your models here

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    polls = Nested('PollSchema', many=True)
    votes = Nested('VoteSchema', many=True)

class PollSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Poll
        include_relationships = True
        load_instance = True

    user = Nested('UserSchema')
    options = Nested('OptionSchema', many=True)
    votes = Nested('VoteSchema', many=True)

class VoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vote
        include_relationships = True
        load_instance = True

    user = Nested('UserSchema')
    option = Nested('OptionSchema')
    poll = Nested('PollSchema')

class OptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Option
        include_relationships = True
        load_instance = True

    poll = Nested('PollSchema')
    votes = Nested('VoteSchema', many=True)
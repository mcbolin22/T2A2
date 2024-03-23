from init import db, ma
from .schemas import VoteSchema
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# from .user import UserSchema
# from .poll import PollSchema
# from .option import OptionSchema

class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)

    user = db.relationship('User', back_populates='votes')
    option = db.relationship('Option', back_populates='votes')
    poll = db.relationship('Poll', back_populates='votes')

class VoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vote
        include_relationships = True
        load_instance = True

    id = auto_field(dump_only=True)  # Only include in responses (security)
    user_id = auto_field()
    option_id = auto_field()
    poll_id = auto_field()
    user = Nested('UserSchema')
    option = Nested('OptionSchema')
    poll = Nested('PollSchema')

vote_schema = VoteSchema()
votes_schema = VoteSchema(many=True)
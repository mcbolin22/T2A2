from init import db, ma
from .schemas import OptionSchema
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# from .vote import VoteSchema
# from .poll import PollSchema

class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))

    poll = db.relationship('Poll', back_populates='options')
    votes = db.relationship('Vote', back_populates='option')

class OptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Option
        include_relationships = True
        load_instance = True

    id = auto_field()
    text = auto_field()
    poll_id = auto_field()
    poll = Nested('PollSchema')
    votes = Nested('VoteSchema', many=True)

option_schema = OptionSchema()
options_schema = OptionSchema(many=True)
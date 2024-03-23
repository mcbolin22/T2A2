from datetime import datetime
from .schemas import PollSchema
from marshmallow import fields, validates, Schema
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# from .option import OptionSchema
# from .vote import VoteSchema


from init import db, ma
# from .user import UserSchema

class Poll(db.Model):
    __tablename__ = "polls"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="polls")
    options = db.relationship("Option", back_populates="poll")
    votes = db.relationship('Vote', back_populates='poll', lazy=True)

class PollSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Poll
        include_relationships = True
        load_instance = True

    id = auto_field()
    title = auto_field()
    description = auto_field()
    created_at = auto_field()
    user_id = auto_field()
    user = Nested('UserSchema')  # Use string here
    options = Nested('OptionSchema', many=True)
    votes = Nested('VoteSchema', many=True)

    @ma.post_load
    def make_poll(self, data, **kwargs):
        self.fields["user"].schema = 'UserSchema()'  # Set the schema here
        return data

poll_schema = PollSchema()
polls_schema = PollSchema(many=True)
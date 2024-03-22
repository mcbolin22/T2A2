from datetime import datetime
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

class Poll(db.Model):
    __tablename__ = "polls"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="polls")
    options = db.relationship("Option", back_populates="polls")
    votes = db.relationship("Vote", back_populates="polls")

class PollSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True, validate=And(
        Length(min=2, error="Title must be at least 2 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$', error="Title can only have alphanumeric characters")
    ))
    description = fields.String()
    created_at = fields.DateTime()
    user_id = fields.Integer()

    class Meta:
        fields = ('id', 'title', 'description', 'created_at', 'user')
    

poll_schema = PollSchema()
polls_schema = PollSchema(many=True)
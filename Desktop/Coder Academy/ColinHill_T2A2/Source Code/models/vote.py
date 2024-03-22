from init import db, ma
from marshmallow import Schema, fields

class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))

    user = db.relationship('User', back_populates='votes')
    poll = db.relationship("Poll", back_populates="votes")
    option = db.relationship('Option', back_populates='votes')

class VoteSchema(ma.Schema):
    id = fields.Integer(dump_only=True)  # Only include in responses (security)
    user_id = fields.Integer()
    option_id = fields.Integer()

vote_schema = VoteSchema()
votes_schema = VoteSchema(many=True)
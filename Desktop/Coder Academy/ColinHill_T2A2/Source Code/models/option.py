from init import db, ma
from marshmallow import fields

class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))

    poll = db.relationship('Poll', back_populates='options')
    votes = db.relationship('Vote', back_populates='option')

class OptionSchema(ma.Schema):
    id = fields.Integer()
    text = fields.String()

option_schema = OptionSchema()
options_schema = OptionSchema(many=True)
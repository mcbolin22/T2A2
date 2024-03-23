from init import db, ma
from marshmallow import fields, Schema, post_load  # Import post_load from marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    polls = db.relationship('Poll', backref='user', lazy=True)
    votes = db.relationship('Vote', back_populates='user')


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()
    email = auto_field()
    is_admin = auto_field()
    polls = Nested('PollSchema', many=True)  # Use string here
    votes = Nested('VoteSchema', many=True)

    @post_load  # Use post_load decorator here
    def make_user(self, data, **kwargs):
        self.fields["polls"].schema = 'PollSchema(many=True)'  # Set the schema here
        return data

user_schema = UserSchema()
users_schema = UserSchema(many=True)

from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    polls = db.relationship("Poll", back_populates="users")



class UserSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    is_admin = fields.Boolean()

    class Meta:
        fields = ('id', 'name', 'email', 'is_admin')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

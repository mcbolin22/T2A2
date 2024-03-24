from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User
from models.schemas import user_schema

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/register", methods=["POST"]) # /auth/register
def user_register():
    try:
        # the data that we get in body of the request
        body_data = request.get_json()

        # validate and deserialize input
        user_data = user_schema.load(body_data)

        # create the user instance
        user = User(
            name=user_data.get('name'),
            email=user_data.get('email')
        )

        # add and commit the user to DB
        db.session.add(user)
        db.session.commit()
        # Repond back to the client
        return user_schema.dump(user), 201

    except ValidationError as err:
        return {"error": err.messages}, 400  # return validation errors
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409

    
@user_bp.route("/login", methods=["POST"]) # /auth/login
def user_login():
    # get the data from the request body
    body_data = request.get_json()
    # Find the user with the email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user:
        return {"email": user.email, "is_admin": user.is_admin}
    else:
        return {"error": "Invalid email"}, 401
    

@user_bp.route("/users", methods=["GET"])
@jwt_required()  # Ensure JWT authentication is required
def get_all_users():
  current_user_id = get_jwt_identity()
  if not current_user_id.is_admin:
    return {"error": "Unauthorized: Admin access required"}, 403

  # Get all users from the database
  users = User.query.all()
  # Return the list of users serialized with the user schema
  return user_schema.dump(users, many=True), 200

@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()  # Ensure JWT authentication is required
def get_user_by_id(user_id):
  current_user_id = get_jwt_identity()
  if not current_user_id.is_admin and current_user_id != user_id:
    return {"error": "Unauthorized: Access restricted to admins or own profile"}, 403

  # Get the user by ID
  user = User.query.get(user_id)
  if not user:
    return {"error": f"User not found with ID: {user_id}"}, 404

  # Return the user serialized with the user schema
  return user_schema.dump(user), 200


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()  # Ensure JWT authentication is required
def delete_user(user_id):
  current_user_id = get_jwt_identity()
  if not current_user_id.is_admin:
    return {"error": "Unauthorized: Admin access required"}, 403

  # Get the user by ID
  user = User.query.get(user_id)
  if not user:
    return {"error": f"User not found with ID: {user_id}"}, 404

  # Delete the user from the database
  db.session.delete(user)
  db.session.commit()

  # Return a success message
  return {"message": f"User ID {user_id} deleted successfully"}, 200
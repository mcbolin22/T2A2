from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from init import db
from models.user import User, user_schema, users_schema
from models.poll import Poll, polls_schema, poll_schema
from models.option import Option, option_schema, options_schema
from models.vote import Vote, vote_schema

polls_bp = Blueprint('polls', __name__, url_prefix='/polls')

@polls_bp.route('/', methods=['GET'])
def get_all_polls():
    try:
        stmt = db.select(Poll).order_by(Poll.created_at.desc())
        polls = db.session.scalars(stmt)
        return polls_schema.dump(polls)
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls', methods=['GET'])
@jwt_required()
def get_polls():
    try:
        polls = Poll.query.all()
        return polls_schema.dump(polls), 200
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls/<int:poll_id>', methods=['GET'])
@jwt_required()
def get_poll(poll_id):
    try:
        poll = Poll.query.get(poll_id)
        if not poll:
            return {'error': f"Poll not found with ID: {poll_id}"}, 404
        return poll_schema.dump(poll, include_options=True), 200
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500
    

@polls_bp.route('/polls/<int:poll_id>/results', methods=['GET'])
@jwt_required()
def get_poll_results(poll_id):
  try:
    # Get the poll by ID
    poll = Poll.query.get(poll_id)
    if not poll:
      return jsonify({'error': f"Poll not found with ID: {poll_id}"}, 404)

    # Calculate vote counts for each option
    option_results = (
        db.session
        .query(Option.id, Option.text, db.func.count(Vote.id).label('vote_count'))
        .join(Vote, Option.id == Vote.option_id)
        .filter(Vote.poll_id == poll.id)
        .group_by(Option.id, Option.text)
        .all()
    )

    # Return poll details and vote counts
    results = {
        'poll': poll_schema.dump(poll),
        'options': options_schema.dump(option_results, many=True),
    }
    return jsonify(results), 200
  except Exception as err:
    # Handle database or other unexpected errors
    return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls', methods=['POST'])
@jwt_required()
def create_poll():
    try:
        # Validate data (e.g., required fields, data types)
        body_data = request.get_json()
        if not body_data or 'title' not in body_data:
            return jsonify({'error': 'Missing required field: title'}), 400

        title = body_data.get('title')
        description = body_data.get('description')

        # No additional permission check needed for basic user creation

        poll = Poll(
            title=title,
            description=description,
            user_id=get_jwt_identity()
        )

        db.session.add(poll)
        db.session.commit()

        return poll_schema.dump(poll), 201
    except IntegrityError as err:
        # Handle potential duplicate entry errors
        return jsonify({'error': f'Conflict: {str(err)}'}), 409
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls/<int:poll_id>', methods=['PUT'])
@jwt_required()
def update_poll(poll_id):
    try:
        # Validate data (e.g., required fields, data types)
        body_data = request.get_json()
        if not body_data:
            return jsonify({'error': 'Missing data'}), 400

        title = body_data.get('title')
        description = body_data.get('description')

        # Check permission to update poll (creator or admin)
        current_user_id = get_jwt_identity()
        poll = Poll.query.get(poll_id)
        if not poll:
            return jsonify({'error': f"Poll not found with ID: {poll_id}"}), 404

        # Check if user is creator of the poll or an admin
        is_creator = poll.user_id == current_user_id
        current_user = User.query.get(current_user_id)  # Assuming you have a User model
        is_admin = current_user and current_user.is_admin  # Check for admin role (optional)

        if not (is_creator or is_admin):
            return jsonify({'error': 'Unauthorized to update poll'}), 401

        poll.title = title or poll.title
        poll.description = description or poll.description

        db.session.commit()

        return poll_schema.dump(poll), 200
    except IntegrityError as err:
        # Handle potential duplicate entry errors
        return jsonify({'error': f'Conflict: {str(err)}'}), 409
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls/<int:poll_id>', methods=['DELETE'])
@jwt_required()
def delete_poll(poll_id):
    try:
        # Check permission to delete poll (creator or admin)
        current_user_id = get_jwt_identity()
        poll = Poll.query.get(poll_id)
        if not poll:
            return jsonify({'error': 'Poll not found'}), 404

        # Check if user is creator of the poll or an admin
        is_creator = poll.user_id == current_user_id
        current_user = User.query.get(current_user_id)  # Assuming you have a User model
        is_admin = current_user and current_user.is_admin  # Check for admin role (optional)

        if not (is_creator or is_admin):
            return jsonify({'error': 'Unauthorized to delete poll'}), 401

        db.session.delete(poll)
        db.session.commit()

        return jsonify({'message': f"Poll with ID: {poll_id} deleted successfully"}), 200
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls/<int:poll_id>/options', methods=['POST'])
@jwt_required()
def create_option(poll_id):
    try:
        # Validate data (e.g., required fields, data types)
        body_data = request.get_json()
        if not body_data or 'text' not in body_data:
            return jsonify({'error': 'Missing required field: text'}), 400

        text = body_data.get('text')

        # Check permission to add options (creator or admin)
        current_user_id = get_jwt_identity()
        poll = Poll.query.get(poll_id)
        if not poll:
            return jsonify({'error': f"Poll not found with ID: {poll_id}"}), 404

        # Check if user is creator of the poll or an admin
        current_user = User.query.get(current_user_id)  # Assuming you have a User model
        is_admin = current_user and current_user.is_admin  # Check for admin role (optional)
        is_creator = poll.user_id == current_user_id

        if not (is_creator or is_admin):
            return jsonify({'error': 'Unauthorized to add options'}), 401

        # Create a new option instance for the poll
        option = Option(text=text, poll_id=poll.id)

        db.session.add(option)
        db.session.commit()

        # Return the newly created option
        return option_schema.dump(option), 201
    except IntegrityError as err:
        # Handle potential duplicate entry errors
        return jsonify({'error': f'Conflict: {str(err)}'}), 409
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls/<int:poll_id>/options/<int:option_id>', methods=['DELETE'])
@jwt_required()
def delete_option(poll_id, option_id):
    try:
        # Check permission to delete option (creator of poll or admin)
        current_user_id = get_jwt_identity()
        poll = Poll.query.get(poll_id)
        if not poll:
            return jsonify({'error': 'Poll not found'}), 404

        # Get the option from the database by ID
        option = Option.query.get((poll_id, option_id))
        if not option:
            return jsonify({'error': f"Option not found with ID: {option_id}"}), 404

        # Check if user is creator of the poll or an admin
        current_user = User.query.get(current_user_id)  # Assuming you have a User model
        is_admin = current_user and current_user.is_admin  # Check for admin role (optional)
        is_creator = poll.user_id == current_user_id  # Check if user created the poll

        if not (is_creator or is_admin):
            return jsonify({'error': 'Unauthorized to delete option'}), 401

        db.session.delete(option)
        db.session.commit()

        # Return success message
        return jsonify({'message': f"Option with ID: {option_id} deleted successfully"}), 200
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500


@polls_bp.route('/polls/<int:poll_id>/vote', methods=['POST'])
@jwt_required()
def vote(poll_id):
    try:
        # Validate data (e.g., required fields, data types)
        body_data = request.get_json()
        if not body_data or 'option_id' not in body_data:
            return jsonify({'error': 'Missing required field: option_id'}), 400

        option_id = body_data.get('option_id')

        # Get the option from the database by ID
        option = Option.query.get(option_id)
        if not option:
            return jsonify({'error': f"Option not found with ID: {option_id}"}), 404

        # Check if user already voted in this poll
        user_id = get_jwt_identity()
        existing_vote = Vote.query.filter_by(poll_id=poll_id, user_id=user_id).first()
        if existing_vote:
            return jsonify({'error': "You already voted in this poll"}), 409

        # Create a new vote instance for the option and user
        vote = Vote(option_id=option_id, user_id=user_id)

        db.session.add(vote)
        db.session.commit()

        # Return success message
        return jsonify({'message': "Vote submitted successfully"}), 201
    except Exception as err:
        # Handle database or other unexpected errors
        return jsonify({'error': str(err)}), 500
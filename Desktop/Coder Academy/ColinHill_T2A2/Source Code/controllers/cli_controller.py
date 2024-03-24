from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.poll import Poll
from models.option import Option
from models.vote import Vote

db_commands = Blueprint('db', __name__)

# This command creates all tables in the database
@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")

# This command drops all tables in the database
@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

# This command seeds the database with initial data
@db_commands.cli.command('seed')
def seed_tables():
    # Create two users
    users = [
        User(
            name="admin",
            email="admin@email.com",
            is_admin=True
        ),
        User(
            name="User 1",
            email="user1@email.com"
        )
    ]
    
    # Add the users to the session and commit the session
    db.session.add_all(users)
    db.session.commit()

    # Query the database to get the two users
    user1 = User.query.filter_by(name="admin").first()
    user2 = User.query.filter_by(name="User 1").first()

    # Create two polls, one for each user
    polls = [
        Poll(
            title="Poll 1",
            description="Poll 1 desc",
            created_at=date.today(),
            user=user1.id
        ),
        Poll(
            title="Poll 2",
            description="Poll 2 desc",
            created_at=date.today(),
            user=user2.id
        )
    ]

    # Add the polls to the session and commit the session
    db.session.add_all(polls)
    db.session.commit()

    # Query the database to get the two polls
    poll1 = Poll.query.filter_by(title="Poll 1").first()
    poll2 = Poll.query.filter_by(title="Poll 2").first()

    # Create two options, one for each poll
    options = [
        Option(
            text="Option 1",
            poll=poll1.id
        ),
        Option(
            text="Option 2",
            poll=poll2.id
        )
    ]

    # Add the options to the session and commit the session
    db.session.add_all(options)
    db.session.commit()

    # Query the database to get the two options
    option1 = Option.query.filter_by(text="Option 1").first()
    option2 = Option.query.filter_by(text="Option 2").first()

    # Create two votes, one for each user and option
    votes = [
        Vote(
            user_id=user1.id,
            option_id=option1.id
        ),
        Vote(
            user_id=user2.id,
            option_id=option2.id
        )
    ]

    # Add the votes to the session and commit the session
    db.session.add_all(votes)
    db.session.commit()

    print("Tables seeded")
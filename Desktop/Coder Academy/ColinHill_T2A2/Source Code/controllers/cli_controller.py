from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.poll import Poll
from models.option import Option
from models.vote import Vote

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")
@db_commands.cli.command('seed')
def seed_tables():
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
    
    db.session.add_all(users)
    db.session.commit()

    user1 = User.query.filter_by(name="admin").first()
    user2 = User.query.filter_by(name="User 1").first()

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

    db.session.add_all(polls)
    db.session.commit()

    poll1 = Poll.query.filter_by(title="Poll 1").first()
    poll2 = Poll.query.filter_by(title="Poll 2").first()

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

    db.session.add_all(options)
    db.session.commit()

    option1 = Option.query.filter_by(text="Option 1").first()
    option2 = Option.query.filter_by(text="Option 2").first()

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

    db.session.add_all(votes)
    db.session.commit()

    print("Tables seeded")
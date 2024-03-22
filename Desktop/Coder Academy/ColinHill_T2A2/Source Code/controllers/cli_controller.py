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
    polls = [
        Poll(
            title="Poll 1",
            description="Poll 1 desc",
            created_at=date.today(),
            user=users[0]
        ),
        Poll(
            title="Poll 2",
            description="Poll 2 desc",
            created_at=date.today(),
            user=users[1]
        )
    ]

    db.session.add_all(polls)
    db.session.commit()
    options = [
        Option(
            text="Option 1",
            poll=polls[0]
        ),
        Option(
            text="Option 2",
            poll=polls[1]
        )
    ]

    db.session.add_all(options)
    db.session.commit()
    votes = [
        Vote(
            user_id=users[0],
            option_id=options[0]
        ),
        Vote(
            user_id=users[1],
            option_id=options[1]
        )
    ]

    db.session.add_all(votes)



    db.session.commit()

    print("Tables seeded")

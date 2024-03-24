import os

from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    # configs
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from controllers.poll_controller import polls_bp
    app.register_blueprint(polls_bp)

    with app.app_context():
        from models.user import User  # import User model
        from models.poll import Poll  # import Poll model
        from models.vote import Vote  # import Vote model
        from models.option import Option
        from models.schemas import UserSchema, PollSchema, VoteSchema, OptionSchema  # import all your schemas here
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
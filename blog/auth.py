import click
from blog.database import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_simplelogin import SimpleLogin


def create_user(**data):
    """Create user with encrypted password."""
    if "username" not in data or "password" not in data:
        raise ValueError("username and password are required.")

    data["password"] = generate_password_hash(
        data.pop("password"), method="pbkdf2:sha256"
    )

    # TODO: Verificar se usuário já existe
    mongo.db.users.insert_one(data)

    return data


def validate_login(user: dict):
    """Validates user login."""
    if "username" not in user or "password" not in user:
        raise ValueError("username and password are required.")

    db_user = mongo.db.users.find_one({"username": user["username"]})
    if db_user and check_password_hash(db_user['password'], user['password']):
        return True

    return False


def configure(app):
    SimpleLogin(app, login_checker=validate_login)

    @app.cli.command()
    @click.argument("username")
    @click.password_option()
    def add_user(username, password):
        """Create a new user"""
        user = create_user(username=username, password=password)
        click.echo(f"User created {user['username']}")

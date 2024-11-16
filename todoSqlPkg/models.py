# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    """ User model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'


class Todos(db.Model):
    """ Todos model """
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(microsecond=0), nullable=False)

    def __repr__(self):
        return f'<Todo: {self.title} || {self.description} || {self.completed} || {self.date_created}>'


def save_user(user, password):
    # password_hash = generate_password_hash(password)
    # users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})
    pass


def save_todo(title, description, completed, data_created):
    pass


# def get_user(username):
#     # user_data = users_collection.find_one({'_id': username})
#     # return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None
#     user_object = User.query.filter_by(username=username).first()
#     return user_object if user_object else None


def get_password(username):
    # user_data = users_collection.find_one({'_id': username})
    # return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None
    pass


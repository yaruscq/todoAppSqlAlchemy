# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Use pytz if on Python <3.9


db = SQLAlchemy()

class User(db.Model):
    """ User model """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'
    
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True  # You can add more complex logic if needed

    def is_active(self):
        """Return True if the user account is active."""
        return self.active

    def is_anonymous(self):
        """Return False because this is not an anonymous user."""
        return False

    def get_id(self):
        # Flask-Login uses this to identify the user. Return username instead of id.
        """Return the unique identifier for the user."""
        return self.username  # Or self.id if you prefer
    

class Todos(db.Model):
    """ Todos model """
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Taipei')).replace(microsecond=0), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    # date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(microsecond=0), nullable=False)
    # date_created = db.Column(
    #     db.DateTime,
    #     default=lambda: datetime.now(timezone('Asia/Taipei')).replace(microsecond=0),
    #     nullable=False
    # )

    def __repr__(self):
        return f'<Todo: {self.title} || {self.description} || {self.completed} || {self.date_created}>'
    
    


def save_user(user, password):
    # password_hash = generate_password_hash(password)
    # users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})
    pass


def save_todo(title, description, completed, data_created):
    pass





def get_password(username):
    # user_data = users_collection.find_one({'_id': username})
    # return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None
    pass


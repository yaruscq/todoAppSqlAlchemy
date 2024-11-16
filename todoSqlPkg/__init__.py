from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='secret_key'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'
    from .models import db, User
    db.init_app(app)

    
    app.register_blueprint(main)

    from .extensions import login_manager
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    from tickets import routes  # Import routes

    return app

app = create_app()

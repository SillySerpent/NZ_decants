import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker

from webpage.adapters.csv_data_reader.csv_data_reader import CsvDataReader
from webpage.adapters.db_methods.db_repository import SqlAlchemyRepository

db = SQLAlchemy()


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    database_uri = "sqlite://cologne_data.db"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cologne_data.db'  # Update this with your DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications for performance

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        from webpage.home_page import home_page
        app.register_blueprint(home_page.home_page_blueprint)

        from webpage.browse_page import browse_page
        app.register_blueprint(browse_page.browse_page_blueprint)

        # Create the database and tables if they don't exist
        db.create_all()

        # Initialize CsvDataReader and populate database
        data_reader = CsvDataReader(db)  # If your file is not in the default location, change this
        data_reader.populate_db(app)  # Populates the DB with data from the CSV

    return app

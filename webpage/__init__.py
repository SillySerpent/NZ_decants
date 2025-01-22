import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect

from webpage.adapters.csv_data_reader.csv_data_reader import CsvDataReader
from webpage.adapters.db_methods.db_repository import SqlAlchemyRepository

import webpage.adapters.repository as repo

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    database_uri = 'sqlite:///cologne.db'

    # Set the URI for your SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    # Initialize the app with the database extension
    db.init_app(app)

    with app.app_context():
        # Check if the SQLite database exists
        if not os.path.exists('cologne.db'):
            print("Database file does not exist. Creating it now.")

        # Attempt to create the tables
        if not inspect(db.engine).has_table('cologne'):
            print("Table 'cologne' does not exist. Creating it now...")
            db.create_all()  # Create tables if they do not exist
            data_reader = CsvDataReader(db)
            data_reader.populate_db()  # Populate database with initial data
            print("Database and table creation completed.")
        else:
            print("Table 'cologne' already exists.")

        # Register blueprints for modular routing
        from webpage.home_page import home_page
        app.register_blueprint(home_page.home_page_blueprint)

        from webpage.browse_page import browse_page
        app.register_blueprint(browse_page.browse_page_blueprint)

    return app

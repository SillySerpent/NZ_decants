import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

from webpage.adapters.csv_data_reader.csv_data_reader import CsvDataReader
from webpage.adapters.db_methods.db_repository import SqlAlchemyRepository
import webpage.adapters.repository as repo
from webpage.adapters.db_methods.populate_db import populate_db
from webpage.domain_model.domain_model import db


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    # Define paths and configurations
    db_name = 'webpage_database.db'
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    # Initialize SQLAlchemy
    db.init_app(app)

    # Create a session factory
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session_factory = scoped_session(Session)

    with app.app_context():
        # Check if the database exists, create it if not
        if not os.path.exists(db_name):
            print(f"Database '{db_name}' does not exist. Creating it now...")
            db.create_all()  # Create all tables
            populate_db(session_factory)
            print(f"Database '{db_name}' initialized and populated.")
        else:
            print(f"Database '{db_name}' already exists. Checking tables...")

        # Verify schema
        table_names = inspect(engine).get_table_names()
        if 'cologne' not in table_names:
            print("Table 'cologne' does not exist. Creating all tables...")
            db.create_all()
        else:
            print("All necessary tables are already in place.")

        # Set up repository with session factory
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        # Register blueprints
        from webpage.home_page import home_page
        app.register_blueprint(home_page.home_page_blueprint)

        from webpage.browse_page import browse_page
        app.register_blueprint(browse_page.browse_page_blueprint)

        from webpage.cart import cart
        app.register_blueprint(cart.cart_blueprint)

    return app


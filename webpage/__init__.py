import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy import inspect

# Import your models and repositories
from webpage.adapters.db_methods.populate_db import populate_db
from webpage.adapters.db_methods.db_repository import SqlAlchemyRepository
import webpage.adapters.repository as repo
from webpage.domain_model.domain_model import db  # Assuming db is your SQLAlchemy instance

def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    # --- Configuration ---
    db_name = 'webpage_database.db'
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key

    # --- Initialize Extensions ---
    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Redirect to login page if not authenticated
    login_manager.login_message_category = 'info'

    # --- User Loader for LoginManager ---
    from webpage.domain_model.domain_model import User  # Adjust based on your actual user model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # --- Database Initialization ---
        if not os.path.exists(db_path):
            print(f"Database '{db_name}' does not exist. Creating it now...")
            db.create_all()  # Create all tables
            populate_db(db.session)  # Use db.session provided by Flask-SQLAlchemy
            print(f"Database '{db_name}' initialized and populated.")
        else:
            print(f"Database '{db_name}' already exists. Checking tables...")

            # Verify schema
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()
            if 'cologne' not in table_names:
                print("Table 'cologne' does not exist. Creating all tables...")
                db.create_all()
            else:
                print("All necessary tables are already in place.")

        # --- Set up repository ---
        repo.repo_instance = SqlAlchemyRepository(db.session)

        # --- Register Blueprints ---
        from webpage.home_page import home_page
        app.register_blueprint(home_page.home_page_blueprint)

        from webpage.browse_page import browse_page
        app.register_blueprint(browse_page.browse_page_blueprint)

        from webpage.cart import cart
        app.register_blueprint(cart.cart_blueprint)

        # Add blueprints for authentication
        from webpage.auth import auth
        app.register_blueprint(auth.auth_blueprint)

    return app


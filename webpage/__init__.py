from flask import Flask


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():

        from webpage.home_page import home_page
        app.register_blueprint(home_page.home_page_blueprint)

        from webpage.browse_page import browse_page
        app.register_blueprint(browse_page.browse_page_blueprint)

    return app

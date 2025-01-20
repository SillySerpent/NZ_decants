from flask import Blueprint, render_template

browse_page_blueprint = Blueprint(
    'browse_page_blueprint', __name__)

@browse_page_blueprint.route("/browse_page", methods=['GET', 'POST'])
def browse_page():
    return render_template("browse_page.html")
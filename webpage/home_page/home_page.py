from flask import Blueprint, render_template


home_page_blueprint = Blueprint(
    'home_page_blueprint', __name__)

@home_page_blueprint.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template("main_menu.html")



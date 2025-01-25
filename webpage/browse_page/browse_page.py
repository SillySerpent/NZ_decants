from flask import Blueprint, render_template
from webpage.adapters.db_methods.db_repository import SqlAlchemyRepository
from webpage.adapters.repository import repo_instance as repo

browse_page_blueprint = Blueprint(
    'browse_page_blueprint', __name__)

@browse_page_blueprint.route("/browse_page", methods=['GET', 'POST'])
def browse_page():
    colognes = repo.get_all_colognes()
    for cologne in colognes:
        print(f"Debug: {cologne.name}, {cologne.notes}")
    return render_template("browse_page.html", colognes=colognes)

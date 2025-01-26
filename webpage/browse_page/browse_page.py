from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from webpage.adapters.repository import repo_instance as repo
from webpage.cart.cart import cart_blueprint
from webpage.browse_page.services import add_cologne_to_cart

browse_page_blueprint = Blueprint(
    'browse_page_blueprint', __name__)

@browse_page_blueprint.route("/browse_page", methods=['GET', 'POST'])
def browse_page():
    colognes = repo.get_all_colognes()
    for cologne in colognes:
        print(f"Debug: {cologne.name}, {cologne.notes}")
    return render_template("browse_page.html", colognes=colognes)


@browse_page_blueprint.route('/browse_page/add_to_cart/<int:cologne_id>', methods=['POST'])
@login_required
def add_to_cart(cologne_id):
    quantity = int(request.form.get('quantity', 1))
    try:
        add_cologne_to_cart(cologne_id, quantity)
        flash('Item added to cart successfully!', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('authentication_blueprint.login', cologne_id=cologne_id))

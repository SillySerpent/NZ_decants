from flask import Blueprint, render_template
from flask_login import login_required

cart_blueprint = Blueprint(
    'cart_blueprint', __name__)


@cart_blueprint.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    return render_template("cart.html")

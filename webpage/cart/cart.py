from flask import Blueprint, render_template
from flask_login import login_required

from webpage.cart.services import get_colognes_from_cart
from webpage.domain_model.domain_model import Cart

cart_blueprint = Blueprint(
    'cart_blueprint', __name__)



@cart_blueprint.route('/cart', methods=['GET'])
@login_required
def view_cart():
    colognes = get_colognes_from_cart()
    return render_template('cart.html', colognes=colognes)




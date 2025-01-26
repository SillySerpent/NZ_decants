from flask import flash
from flask_login import current_user

from webpage.domain_model.domain_model import Cart, db, Cologne, CartItem


def get_or_create_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()  # Commit to generate an ID for the new cart
    return cart




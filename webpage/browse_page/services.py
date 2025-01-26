from flask import flash
from flask_login import current_user

from webpage.domain_model.domain_model import Cart, db, Cologne, CartItem


def add_cologne_to_cart(cologne_id: int, quantity: int = 1):
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    cologne = Cologne.query.get(cologne_id)
    if not cologne:
        raise ValueError(f"Cologne with ID {cologne_id} does not exist.")

    # Retrieve or create the cart
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()  # Commit to assign an ID to the cart

    # Add the cologne to the cart
    existing_item = next((item for item in cart.items if item.cologne_id == cologne_id), None)
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(cart_id=cart.id, cologne_id=cologne_id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()

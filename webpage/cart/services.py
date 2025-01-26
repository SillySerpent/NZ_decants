from typing import List

from flask_login import current_user
from webpage.domain_model.domain_model import Cart, CartItem, Cologne, db
import webpage.adapters.repository as repo

from flask import abort


def get_colognes_from_cart() -> List[Cologne]:
    if not current_user.is_authenticated:
        abort(401)  # Unauthorized access

    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if not cart:
        return []

    colognes = [
        repo.repo_instance.get_cologne_by_id(item.cologne_id)
        for item in cart.items
    ]

    return colognes

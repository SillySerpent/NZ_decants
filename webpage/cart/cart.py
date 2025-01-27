from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf, CSRFError
import webpage.adapters.repository as repo

cart_blueprint = Blueprint('cart_blueprint', __name__)


@cart_blueprint.route('/view_cart', methods=['GET'])
@login_required
def view_cart():
    user_id = current_user.id
    colognes = repo.repo_instance.get_cart_items_by_user_id(user_id=user_id)
    return render_template('cart.html', cart_items=colognes)



@cart_blueprint.route('/view_cart/remove_cologne/<int:cologne_id>', methods=['POST'])
@login_required
def remove_cologne(cologne_id):
    csrf_token = request.form.get('csrf_token')
    try:
        validate_csrf(csrf_token)
        repo.repo_instance.remove_cologne_from_cart(user_id=current_user.id, cologne_id=cologne_id)
    except CSRFError as e:
        print(e)
    return redirect(url_for('cart_blueprint.view_cart'))


@cart_blueprint.route('/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    try:
        data = request.get_json()
        cologne_id = data.get('cologne_id')
        quantity = data.get('quantity')
        csrf_token = request.headers.get('X-CSRFToken')
        validate_csrf(csrf_token)
        print(f"Updating cologne_id {cologne_id} to quantity {quantity} for user {current_user.id}")
        repo.repo_instance.update_cart_item_quantity(
            user_id=current_user.id,
            cologne_id=cologne_id,
            quantity=quantity
        )
        return jsonify({'success': True}), 200
    except Exception as e:
        import traceback
        print("Exception in /update_quantity:")
        print(traceback.format_exc())
        return jsonify({'success': False}), 400

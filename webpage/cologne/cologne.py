# blueprints/cologne_blueprint.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from webpage import db
from webpage.domain_model.domain_model import Cologne, Review

cologne_blueprint = Blueprint('cologne_blueprint', __name__, template_folder='../templates')


@cologne_blueprint.route('/cologne/<int:cologne_id>', methods=['GET', 'POST'])
def cologne_page(cologne_id):
    # Fetch the cologne from the database
    cologne = Cologne.query.get_or_404(cologne_id)

    # Fetch related fragrance notes
    fragrance_notes = cologne.notes

    # Fetch reviews for the cologne
    reviews = Review.query.filter_by(cologne_id=cologne_id)

    return render_template("cologne.html", cologne=cologne, fragrance_notes=fragrance_notes,)


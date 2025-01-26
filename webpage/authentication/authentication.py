from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from webpage.domain_model.domain_model import User
from webpage.forms_and_routs.forms import LoginForm


authentication_blueprint = Blueprint('authentication_blueprint', __name__)

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page_blueprint.home_page'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            login_user(user)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page_blueprint.home_page'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)
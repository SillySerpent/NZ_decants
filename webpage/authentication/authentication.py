from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from webpage.domain_model.domain_model import User
from webpage.forms_and_routs.forms import RegistrationForm

authentication_blueprint = Blueprint('authentication_blueprint', __name__)

form = RegistrationForm()

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authenticate user
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home_page_blueprint.home_page'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@authentication_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page_blueprint.home_page'))
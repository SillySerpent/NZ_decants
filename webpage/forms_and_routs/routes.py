from flask import render_template, url_for, flash, redirect, request, Blueprint
from webpage import db, bcrypt
from webpage.forms_and_routs.forms import RegistrationForm, LoginForm
from webpage.domain_model.domain_model import User
from flask_login import login_user, current_user, logout_user, login_required


routes_blueprint = Blueprint('routes_blueprint', __name__)

@routes_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page_blueprint.home_page'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please log in.', 'success')
        return redirect(url_for('routes_blueprint.login'))
    return render_template('register.html', form=form)

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page_blueprint.home_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            # Redirect to next page if accessed via @login_required
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page_blueprint.home_page'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@routes_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page_blueprint.home_page'))
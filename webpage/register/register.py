from flask import request, flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash

from webpage.domain_model.domain_model import User, db
from wsgi import app


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Create new user and save to database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')
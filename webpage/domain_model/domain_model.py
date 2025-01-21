from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Cologne(db.Model):
    __tablename__ = 'colognes'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    picture_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    season = db.Column(db.String(50))
    category = db.Column(db.String(50))
    sex = db.Column(db.PickleType())  # Assuming `sex` is a list
    discount = db.Column(db.Integer)
    featured = db.Column(db.Boolean)
    availability = db.Column(db.Boolean)
    rating = db.Column(db.Integer)
    notes = db.Column(db.PickleType())  # Assuming `notes` is a list
    release_year = db.Column(db.Integer)
    concentration = db.Column(db.String(50))




class User(db.Model):  # Inherit from db.Model for SQLAlchemy integration
    __tablename__ = 'users'  # Table name in the database

    # Define table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username must be unique
    password = db.Column(db.String(120), nullable=False)  # Store hashed passwords
    name = db.Column(db.String(120), nullable=False)  # User's name
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email must be unique

    # Relationship to Cart model
    cart = db.relationship('Cart', backref='user', lazy=True)

    def __init__(self, username: str, password: str, id: int, name: str, email: str):
        self.username = username
        self.password = password
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User {self.username}>"


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to users
    items = db.Column(db.PickleType, nullable=True)  # Store items as a serialized list

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __repr__(self):
        return f"<Cart for User {self.user_id}>"

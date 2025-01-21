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


    def __init__(self, id, price, name, size, picture_url, description, season,
                 category, sex, discount, featured, availability, rating,
                 notes, release_year, concentration):
        self.id = id
        self.price = price
        self.name = name
        self.size = size
        self.picture_url = picture_url
        self.description = description
        self.season = season
        self.category = category
        self.sex = sex
        self.discount = discount
        self.featured = featured
        self.availability = availability
        self.rating = rating
        self.notes = notes
        self.release_year = release_year
        self.concentration = concentration


    def __str__(self):
        return (
            f"Cologne: {self.name}\n"
            f"Scent Profile: {self.notes}\n"
            f"Size: {self.size}\n"
            f"Price: ${self.price:.2f}\n"
            f"Description: {self.description}"
            f"\n"
        )

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



class Review(db.Model):

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id: int, item_id: int, rating: int):
        self.user_id = user_id
        self.item_id = item_id
        self.rating = rating


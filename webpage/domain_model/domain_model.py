from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Cologne(db.Model):
    __tablename__ = 'cologne'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    picture_url = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    season = db.Column(db.String, nullable=True)
    sex = db.Column(db.String, nullable=True)
    discount = db.Column(db.Float, nullable=True, default=0.0)
    featured = db.Column(db.Boolean, nullable=True, default=False)
    availability = db.Column(db.Boolean, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    concentration = db.Column(db.String, nullable=True)

    # Relationship to CartItem is established via backref in CartItem model.

    def __init__(self, price, name, size, picture_url, description, season,
                 sex, rating, notes, release_year, concentration):
        self.price = price
        self.name = name
        self.size = size
        self.picture_url = picture_url
        self.description = description
        self.season = season
        self.sex = sex
        self.discount = 0.00
        self.featured = False
        self.availability = True
        self.rating = rating
        self.notes = notes
        self.release_year = release_year
        self.concentration = concentration

    def apply_discount(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return (
            f"Cologne: {self.name}\n"
            f"Scent Profile: {self.notes}\n"
            f"Size: {self.size}ml\n"
            f"Price: ${self.price:.2f}\n"
            f"Description: {self.description}\n"
        )

    def __eq__(self, other):
        return self.id == other.id


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # Relationship to Cart
    cart = db.relationship('Cart', back_populates='user', uselist=False)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password  # Triggers the password setter
        self.email = email

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, candidate_password):
        return check_password_hash(self.password_hash, candidate_password)


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to User
    user = db.relationship('User', back_populates='cart')

    # Relationship to CartItem
    items = db.relationship('CartItem', back_populates='cart', lazy='select')

    def __repr__(self):
        return f"<Cart for User {self.user_id}>"

    def add_item(self, cologne_id: int, quantity: int):
        existing_item = next((item for item in self.items if item.cologne_id == cologne_id), None)
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(cart_id=self.id, cologne_id=cologne_id, quantity=quantity)
            db.session.add(new_item)
        db.session.commit()  # Ensure changes are saved to the database

    def remove_item(self, cologne_id: int):
        try:
            item = CartItem.query.filter_by(cart_id=self.id, cologne_id=cologne_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error removing item from cart: {e}")
            raise

    def clear_cart(self):
        for item in self._items:
            db.session.delete(item)
        db.session.commit()


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    cologne_id = db.Column(db.Integer, db.ForeignKey('cologne.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationship to Cart
    cart = db.relationship('Cart', back_populates='items')

    # Relationship to Cologne
    cologne = db.relationship('Cologne', backref=db.backref('cart_items', lazy='select'))

    def __init__(self, cart_id: int, cologne_id: int, quantity: int):
        self.cart_id = cart_id
        self.cologne_id = cologne_id
        self.quantity = quantity

    def __repr__(self):
        return f"<CartItem Cologne {self.cologne_id} Quantity {self.quantity}>"

    def get_total_price(self):
        return self.cologne.apply_discount() * self.quantity


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')

    # Relationship to OrderItem
    items = db.relationship('OrderItem', backref='order', lazy='select')

    def __init__(self, user_id: int, total_price: float, date, status: str = 'Pending'):
        self.user_id = user_id
        self.total_price = total_price
        self.date = date
        self.status = status

    def __repr__(self):
        return f"<Order {self.id} by User {self.user_id} Status {self.status}>"

    def update_status(self, new_status: str):
        self.status = new_status


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    cologne_id = db.Column(db.Integer, db.ForeignKey('cologne.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_purchase = db.Column(db.Float, nullable=False)

    # Relationship to Cologne
    cologne = db.relationship('Cologne', backref=db.backref('order_items', lazy='select'))

    def __init__(self, order_id: int, cologne_id: int, quantity: int, price_at_purchase: float):
        self.order_id = order_id
        self.cologne_id = cologne_id
        self.quantity = quantity
        self.price_at_purchase = price_at_purchase

    def __repr__(self):
        return f"<OrderItem Cologne {self.cologne_id} Quantity {self.quantity}>"

    def get_total_price(self):
        return self.price_at_purchase * self.quantity


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cologne_id = db.Column(db.Integer, db.ForeignKey('cologne.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    # Relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy='select'))
    cologne = db.relationship('Cologne', backref=db.backref('reviews', lazy='select'))

    def __init__(self, user_id: int, cologne_id: int, rating: int, comment: str = None):
        self.user_id = user_id
        self.cologne_id = cologne_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"<Review User {self.user_id} Cologne {self.cologne_id} Rating {self.rating}>"

    def update_comment(self, new_comment: str):
        self.comment = new_comment

    def update_rating(self, new_rating: int):
        self.rating = new_rating

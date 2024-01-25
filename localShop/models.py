from localShop import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    isAdmin = db.Column(db.Boolean(), nullable = False)
    firstName = db.Column(db.String(120), nullable = False)
    lastName = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(20), nullable = False, unique = True)
    address = db.Column(db.String(200), nullable = False)
    orders = db.relationship("Orders", backref = 'user')

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}','{self.isAdmin}','{self.firstName}','{self.lastName}','{self.phone}','{self.address}')"
    
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    status = db.Column(db.String(10), nullable = False)
    total = db.Column(db.Float, nullable = False)
    items = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"Orders('{self.id}','{self.user_id}','{self.date}','{self.status}','{self.total}')"
    
class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    img = db.Column(db.String(50), nullable = False)
    desc = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"Products('{self.id}','{self.name}', '{self.price}', '{self.quantity}')"
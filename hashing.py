import bcrypt
import base64
from localShop import app, db
from localShop.models import User, Orders, Products
from flask import flash
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
import base64

rsa = RSA.generate(1024)

def password_sh(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# def password_comparison(given, hashed):
#     return bcrypt.checkpw(given, hashed)
# password_checked = bcrypt.check_password_hash(password, user.password)

def checking_login(username, password):
    """
    Tbh I'm not sure if we need the checked box or not cuz it might be easier if we had them
    already registered in the database and then redirect them to the admin page
    """
    # Check user name in database and redirect to homepage or admin page (depending on admin flag in db)
    if (username or password) is None:
        return False

    # Seeing if user is in database
    if User.query.filter_by(username = username).scalar():
        stored_pwd = User.query.filter_by(username = username).scalar().password
        # If user in database, compare the passwords and admin privileges
        if not bcrypt.checkpw(password.encode(), stored_pwd): 
            return "password_err"
    else:
        return "username_err"
    
    # Condition checked, seeing if we redirect user to admin page
    admin = User.query.filter_by(username = username).scalar().isAdmin

    if admin:
        return "admin"
    
    return "user"

def registration(username, password1, password2, email, first, last, phone, address):

    # Checking if any attributes are None
    if (username or password1 or password2 or email or first or last or phone or address) is None:
        return False
    
    # Check if user already exist
    if User.query.filter_by(username = username).scalar():
        return 1
    
    # Check if email already exist
    if User.query.filter_by(email = email).scalar():
        return 2

    if password1 == password2:
        # Add user into the database and redirect to home page to log in
        # Generating private and public key for the user (maybe storing the private key as a txt file)
        
        hashed = password_sh(password1)
        user_add = User(username = username, email = email, password = hashed, isAdmin = False,
                        firstName = first, lastName = last, phone = phone, address = address)
        db.session.add(user_add)
        db.session.commit()
            
        return 0
    
    return 1

def retrieve_products():
    return Products.query.all()

def retrieve_orders(user):
    # user_orders = User.query.filter_by(username = user).first().join(Orders)
    # user_orders = Orders.query.filter_by(user_id = user)
    test = User.query.filter_by(username = user).first().id
    # print(test)
    # print(user_orders)
    user_orders = Orders.query.filter_by(user_id = test)
    return user_orders
    # return test

def alphabetical_sort(flag = False):
    # False flag is normal, true flag is reverse alphabetical sort
    # alpha = Products.query.order_by(Products.name).all()
    if not flag:
        alpha = Products.query.order_by(Products.name).limit(5)

    else:
        alpha = Products.query.order_by(Products.name.desc()).limit(5)

    return alpha

def price_sort(flag = False):
    if not flag:
        price = Products.query.order_by(Products.price).limit(5)
        
    else:
        price = Products.query.order_by(Products.price.desc()).limit(5)

    return price

def letter_filter(letter):
    filtered = Products.query.filter(Products.name.startswith(letter), Products.name.startswith(letter.lower())).limit(5)
    return filtered

# Encryption and decryption of data for payment stuff later
# I think we can store the public keys in the database but idk how to store the private keys
def encrypt_data(data):
    public_key = rsa.public_key()
    cipher = PKCS1_v1_5.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(data.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(encrypt_data):
    private_key = rsa
    cipher = PKCS1_v1_5.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_data), 0)
    return back_text.decode('utf-8')

def get_public_key():
    return rsa.public_key().export_key()
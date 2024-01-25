from flask import render_template, request, redirect, url_for, make_response
from localShop.models import *
from localShop import app, db, session
from hashing import *
import os
from werkzeug.utils import secure_filename

# class Total:
#     def __init__(self):
#         self.total = 0
    
#     def calculating_total(self, value):
#         self.total += value
    
#     def return_total(self):
#         return self.total

@app.route('/')
def startup():
    # total_amount = Total()
    loggedIn = make_response(redirect(url_for('home', loggedIn = 0))) 
    loggedIn.set_cookie('loggedIn', "0")
    session["username"] = None
    session["cart"] = list()
    session["total"] = 0
    # session._permanent = False
    # products = retrieve_products()
    return loggedIn
    # return render_template("home.html", loggedIn = False, products = products)

@app.route('/home')
def home():
    # global current_user
    # if loggedIn == False:
    #     session["username"] = None
    # username = getpass.getuser()
    # print(db.session.name)
     
     
    print(session)
    # if session["username"] is None:
    #     loggedIn = make_response(redirect(url_for('home', loggedIn = 0))) 
    #     loggedIn.set_cookie('loggedIn', "0")
    #     session["username"] = None
    #     session["cart"] = list()
    
    # print(session)
    products = retrieve_products()
    # print("LoggedIn value: ", )
    # print(session["username"])
    loggedIn = request.cookies.get('loggedIn')
    # print("Arrived after login", session)
    print("LoggedIn: ", loggedIn)
    


    # logged in user is 2
    if loggedIn == '2':
        return render_template("home.html", loggedIn = 2, products = products, total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products, total = session["total"])
    
    return render_template("home.html", loggedIn = False, products = products, total = session["total"])

@app.route('/login', methods=["GET", 'POST'])
def login():
    # Confirm users in the database

    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]

        log = checking_login(username, password)
        if log == 'username_err':
            flash("Username does not exist, please try again or register", 'error')
            return redirect(url_for("login"))
        
        elif log == 'password_err':
            flash("Incorrect password, please try again", 'error')
            return redirect(url_for("login"))

        elif log == "admin":
            session["username"] = username
            # return redirect(url_for("admin_page"))
            flash(f"Succesfully logged in as {username} (admin).", 'success')
            # Can change this to admin_page to go to admin menu or add as an extra option 
            loggedIn = make_response(redirect(url_for('admin_page', loggedIn = 1))) 
            loggedIn.set_cookie('loggedIn', '1')
            # loggedIn.set_cookie("user", username)
            return loggedIn

        # Get products from database
        # products = retrieve_products()
        # print("Products in database: ", products)
        # for row in products:
        #     print(row.name, row.price, row.quantity)

        # Sets cookie
        # user = User.query.filter_by(username=username).first()
        # print(user)
        elif log == 'user':
            flash(f"Succesfully logged in as {username}.", 'success')
            session["username"] = username
            print(session["username"])
            loggedIn = make_response(redirect(url_for('home', loggedIn = 2))) 
            loggedIn.set_cookie('loggedIn', '2')

            return loggedIn

    return render_template("login.html", title = "Login Form")

@app.route('/register', methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        usr = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        email = request.form["email"]
        first = request.form["first_name"]
        last = request.form["last_name"]
        phone = request.form["phone"]
        address = request.form["address"]

        res = registration(usr, password1, password2, email, first, last, phone, address)

        if res == 0:
            # current_user = usr
            # print(current_user)
            flash(f"Successfully created user {usr}", 'success')
            session["username"] = usr
            # loggedIn = make_response(redirect(url_for(url_for('home', loggedIn = 2)))) 
            loggedIn = make_response(redirect(url_for('home', loggedIn = 2))) 
            loggedIn.set_cookie('loggedIn', '2')

            return loggedIn
        
        elif res == 1:
            flash("Username Already Exists", 'error')
            return redirect(url_for("register"))
        
        elif res == 2:
            flash("User with that Email already Exists", 'error')
            return redirect(url_for("register"))

    return render_template("register.html", title = "User Registration Form")

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/admin')
def admin_page():
    loggedIn = request.cookies.get('loggedIn')
    if loggedIn == '1':
        return render_template('admin_page.html', title = "Admin Management Menu", loggedIn = 1)
    
    if loggedIn == '2':
        flash("LOL, nice try", 'error')
        return redirect(url_for("home"))
    
    flash("LOL, nice try", 'error')
    return redirect(url_for("home"))
    

@app.route("/logout", methods=["GET", 'POST'])
def logout():
    loggedIn = make_response(redirect(url_for('home', loggedIn = False))) 
    loggedIn.set_cookie('loggedIn', '0')
    session["username"] = None
    session["cart"] = list()
    return loggedIn

@app.route("/filter", methods = ["GET", "POST"])
def filtering_products():
    if request.method == 'POST':
        if request.form.get('action1') == "Alphabetical":
            products = alphabetical_sort()
        elif request.form.get('action2') == 'Reverse Alphabetical':
            products = alphabetical_sort(True)
        elif request.form.get('action3') == "Lowest-Highest Price":
            products = price_sort()
        elif request.form.get('action4') == "Highest-Lowest Price":
            products = price_sort(True)
        elif len(request.form.get("action5")) == 1:
            letter = request.form["action5"].upper()
            if letter.isalpha():
                products = letter_filter(letter)
            else:
                flash("Input is not letter", "error")
                products = retrieve_products()
        else:
            flash("Incorrect length of text in textbox", "error")
            products = retrieve_products()
    
    # products = retrieve_products()
    if session["username"] is not None:
        return render_template("home.html", loggedIn = 2, products = products, total = session["total"])
    
    return render_template("home.html", loggedIn = False, products = products, total = session["total"])

def allowed_file(name):
    return '.' in name and name.rsplit('.',1)[1].lower() in ['png','jpeg', 'jpg']

@app.route("/add_products", methods=['GET','POST'])
def manage_products():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form.get("price")
        amount = request.form.get("amount")
        image = request.files['file']
        desc = request.form["desc"]

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            abspath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(abspath)

            add_product = Products(name = name.capitalize(), price = price, quantity = amount, img = path, desc = desc)
            db.session.add(add_product)
            db.session.commit()

            flash("Successfully added the product named {name}".format(name = name))

        else:
            flash("Please upload .png, .jpeg, or .jpg")

        

    loggedIn = request.cookies.get('loggedIn')
    
    if loggedIn == '2':
        flash("LOL, nice try", 'error')
        return redirect(url_for("home"))

    return render_template('add_products.html', title = "Add Products", loggedIn = 1)

@app.route("/edit_products", methods=['GET','POST'])
def edit_products():
    if request.method == "POST":
        id = request.form["product-ids"]
        name = request.form["new_name"]
        price = request.form.get("new_price")
        amount = request.form.get("new_amount")
        desc = request.form["new_desc"]

        to_edit = Products.query.get(id)
        to_edit.name = name
        to_edit.price = price
        to_edit.quantity = amount
        to_edit.desc = desc
        db.session.commit()
        flash("Successfully updated the product with id {id}".format(id = id))

    loggedIn = request.cookies.get('loggedIn')
    
    if loggedIn == '2':
        flash("LOL, nice try", 'error')
        return redirect(url_for("home"))

    products = [x for x in Products.query.order_by(Products.id).all()]
    products_id = [x.id for x in products]
    products_name = [x.name for x in products]
    products_price = [x.price for x in products]
    products_quantity = [x.quantity for x in products]
    products_desc = [x.desc for x in products]

    return render_template('edit_products.html', title = "Edit Products", loggedIn = 1, products = products_id,
                           old_names = products_name, old_prices = products_price, old_amounts = products_quantity, old_desc = products_desc)

@app.route('/del_products',methods=['GET','POST'])
def del_products():
    if request.method == "POST":
        id = request.form["product-ids"]

        to_del = Products.query.get(id)
        db.session.delete(to_del)
        db.session.commit()

    loggedIn = request.cookies.get('loggedIn')
    
    if loggedIn == '2':
        flash("LOL, nice try", 'error')
        return redirect(url_for("home"))

    products = [x for x in Products.query.order_by(Products.id).all()]
    products_id = [x.id for x in products]
    products_name = [x.name for x in products]
    products_price = [x.price for x in products]
    products_quantity = [x.quantity for x in products]
    products_desc = [x.desc for x in products]

    return render_template('del_products.html', title = "Delete Products", loggedIn = 1, products = products_id,
                           names = products_name, prices = products_price, amounts = products_quantity, descs = products_desc)

@app.route("/manage_orders",methods=['GET','POST'])
def manage_orders():
    if request.method == "POST":
        status = request.form['status2']
        id = request.form['order-ids']

        to_edit = Orders.query.get(id)
        to_edit.status = status
        db.session.commit()
        flash("Successfully updated the order with id {id}".format(id = id))

    loggedIn = request.cookies.get('loggedIn')
    
    if loggedIn == '2':
        flash("LOL, nice try", 'error')
        return redirect(url_for("home"))
    
    orders = [x for x in Orders.query.order_by(Orders.id).all()]
    orders_id = [x.id for x in orders]
    orders_user = [x.user_id for x in orders]
    orders_user2 = [User.query.filter(User.id == x).scalar().username for x in orders_user]
    orders_date = [x.date for x in orders]
    orders_status = [x.status for x in orders]
    orders_total = [x.total for x in orders]
    orders_products = [x.items.replace("<br>",", ") for x in orders]

    return render_template('manage_orders.html', title = "Manage Orders", loggedIn = 1, orders = orders_id,
                           names = orders_user2, dates = orders_date, statuses = orders_status, totals = orders_total,
                           orderproducts = orders_products)

@app.route("/order")
def view_orders():
    orders = retrieve_orders(session["username"])
    order_dates = [x.date.strftime("%d/%m/%Y") for x in orders]
    
    return render_template("order.html", title = f"Orders for {session['username']}", loggedIn = 2, orders = orders, dates = order_dates)

@app.route("/testing_cart", methods = ["GET", "POST"])
def testing():
    loggedIn = request.cookies.get('loggedIn')
    
    if request.method == "POST" and loggedIn == '2':
        # Need to add the product to the cart (localStorage)
        id = request.form.get('cart')
        # Access database and retrieve element via id
        adding_to_cart = Products.query.get(id)
        seen = False
        for items in session["cart"]:
            if items[0] == adding_to_cart.name:
                seen = True
                if items[2] < adding_to_cart.quantity:
                    items[2] += 1
                    items[1] = items[2] * adding_to_cart.price
                else:
                    flash(f"{adding_to_cart.name} is out of stock!")
                
        if not seen:
            session["cart"].append([adding_to_cart.name, adding_to_cart.price, 1, adding_to_cart.id])
            session["total"] += adding_to_cart.price
        else:
            session["total"] = 0
            for item in session["cart"]:
                session["total"] += item[1]
            print(session["cart"])
            print("Total cart price: ", session["total"])

    products = retrieve_products()
    print(products)
    print(session["cart"])

    # logged in user is 2
    if loggedIn == '2':
        return render_template("home.html", loggedIn = 2, products = products, cart = session["cart"], total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        flash("Need to be a user to add to cart")
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products, total = session["total"])
    
    else:
        flash("Need to be logged in to add to cart")
        return render_template("home.html", loggedIn = False, products = products, total = session["total"])
    
@app.route("/remove_from_cart", methods = ["GET", "POST"])
def removing_from_cart():  
    loggedIn = request.cookies.get('loggedIn')
    
    if request.method == "POST" and loggedIn == '2':
        # Need to add the product to the cart (localStorage)
        id = request.form.get('remove')
        to_remove = Products.query.get(id)
        for item in session["cart"]:
            if item[0] == to_remove.name:
                item[1] -= to_remove.price
                if item[2] > 1:
                    item[2] -= 1
                else:
                    session["cart"].remove(item)
                session["total"] -= to_remove.price
                break
    
    products = retrieve_products()
    # logged in user is 2
    if loggedIn == '2':
        return render_template("home.html", loggedIn = 2, products = products, cart = session["cart"], total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        flash("Need to be a user to clear cart")
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products)
    
    else:
        flash("Need to be logged in to clear cart")
        return render_template("home.html", loggedIn = False, products = products)
    
@app.route("/clear_cart", methods = ["GET", "POST"])
def clear_cart():
    loggedIn = request.cookies.get('loggedIn')

    if request.method == "POST" and loggedIn == '2':
        if len(session["cart"]) > 0:
            session["cart"] = list()
            flash("Sucessfully cleared cart")

        else:
            flash("Cart is already empty!")

    products = retrieve_products()
    session["total"] = 0
    # logged in user is 2
    if loggedIn == '2':
        return render_template("home.html", loggedIn = 2, products = products, cart = session["cart"], total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        flash("Need to be a user to clear cart")
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products)
    
    else:
        flash("Need to be logged in to clear cart")
        return render_template("home.html", loggedIn = False, products = products)
    
@app.route("/edit_cart_quantity", methods = ["GET","POST"])
def edit_cart_quantity():
    loggedIn = request.cookies.get('loggedIn')

    if request.method == "GET" and loggedIn == '2':

        #  get the parameters from the javascript
        productId = request.args.get('prodId', None)
        productAmount = request.args.get('prodAmt', None)

        # edit the quantity
        for item in session["cart"]:
            if item[3] == int(productId):
                price = round(item[1] / item[2],2)
                item[2] = int(productAmount)
                item[1] = round(price * item[2],2)
                # print("Price: ", price * item[2])
                # # session["total"] += 

        # Update total here
        session["total"] = 0
        for item in session["cart"]:
            session["total"] += item[1]
        print(session["cart"])
        print("Cart total amount: ", session["total"])

    products = retrieve_products()
    # logged in user is 2
    if loggedIn == '2':
        return render_template("home.html", loggedIn = 2, products = products, cart = session["cart"], total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        flash("Need to be a user to add to cart")
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products, total = session["total"])
    
    else:
        flash("Need to be logged in to edit cart")
        return render_template("home.html", loggedIn = False, products = products)

@app.route("/checkout", methods = ["GET","POST"])
def purchase_items():

    loggedIn = request.cookies.get('loggedIn')
    flash("Your payment has been successfully processed!")

    if request.method == "POST" and loggedIn == '2':
        if len(session["cart"]) > 0:

            # Search for user with username in database and add new order in Order table
            username_find = session["username"]
            found = User.query.filter(User.username == username_find).scalar()

            order_products = ""

            if len(session["cart"]) > 1:
                for item in session["cart"]:
                    order_products += f"{item[2]} x {item[0]}<br>"

            else:
                order_products += f"{session['cart'][0][2]} x {session['cart'][0][0]}"

            order_to_add_db = Orders(user_id = found.id, status = "Pending", total = session["total"], items = order_products)
            db.session.add(order_to_add_db)
            db.session.commit()

            for elem in session["cart"]:
                to_edit = Products.query.get(elem[3])
                to_edit.quantity -= int(elem[2])
                db.session.commit()
                
            session["cart"] = list()
            flash("Sucessfully purchased items!")

        else:
            flash("No items to purchase!")

    session["total"] = 0
    products = retrieve_products()
    # logged in user is 2
    if loggedIn == '2':
        return render_template("home.html", loggedIn = 2, products = products, cart = session["cart"], total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        flash("Need to be a user to make a purchase")
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products)
    
    else:
        flash("Need to be logged in to make a purchase")
        return render_template("home.html", loggedIn = False, products = products)

@app.route("/payments")
def payments():
    products = retrieve_products()
    loggedIn = request.cookies.get('loggedIn')

    if loggedIn == '2':
        return render_template("payments.html", loggedIn = 2, products = products, cart = session["cart"], total = session["total"])
    
    # admin is 1
    elif loggedIn == '1':
        flash("Need to be a user to make a purchase")
        return render_template("home.html", title = "Admin Management Menu", loggedIn = 1, products = products)
    
    else:
        flash("Need to be logged in to make a purchase")
        return render_template("home.html", loggedIn = False, products = products)
from localShop import db,app
from hashing import *

app.app_context().push()

db.drop_all()
db.create_all()

list = []

admin_add = User(username = "admin", email = "admin", password = password_sh("admin"), isAdmin = True,
                firstName = "admin", lastName = "admin", phone = "admin", address = "admin")
product_add = Products(name = "Computer", price = 1500.0, quantity = 5, img = r"static\images\Untitled.png", desc = "This is pc.")
product2_add = Products(name = "Phone", price = 1000.0, quantity = 42, img = r"static\images\Untitled.png", desc = "This is phone.")
product3_add = Products(name = "Dog Meat", price = 2.0, quantity = 1234, img = r"static\images\Untitled.png", desc = "This is good food.")
order_add = Orders(user_id = 2, status = "Done", total = 6969.0, items = "4 x Fish")
order_add2 = Orders(user_id = 2, status = "In Progress", total = 100.0, items = "69 x Nice")
order_add3 = Orders(user_id = 2, status = "Pending", total = 9.0, items = "34123 x Peanuts<br>1 x Knife")
user1 = User(username = "user", email = "user", password = password_sh("user"), isAdmin = False,
                firstName = "user", lastName = "user", phone = "user", address = "user")

list.append(admin_add)
list.append(product_add)
list.append(product2_add)
list.append(order_add)
list.append(order_add2)
list.append(order_add3)
list.append(user1)
list.append(product3_add)

for x in list:
    db.session.add(x)

db.session.commit()

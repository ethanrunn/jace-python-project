from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .. import database as db
from .. import utils

admin = Blueprint("admin", __name__)

# LOGIN ROUTE
@admin.route("/")  #/admin/
@admin.route("/login") 
def admin_login():
    if session.get('ADMIN_EMAIL'):
        return redirect(url_for('admin.admin_dashboard'))
        
    return render_template('admin/login.html')

# LOGIN HANDLER
@admin.post("/login_handler")
def admin_login_handler():
    # Check if the fields are empty
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Please fill all fields", "error")
        return redirect(url_for('admin.admin_login'))

    # Check if the email actually exists
    sql = "SELECT * FROM admin WHERE email = %s"
    db.cursor.execute(sql, [email])
    admin = db.cursor.fetchone()

    if not admin:
        flash("Incorrect Credientials", "error")
        return redirect(url_for('admin.admin_login'))

    # print(admin)

    # Check if the passwords match
    if not check_password_hash(admin.get('password'), password):
        flash("Incorrect Credientials", "error")
        return redirect(url_for('admin.admin_login'))

    # Setup a session
    session["ADMIN_EMAIL"] = admin.get('email')

    # Redirect to the dashboard page
    return redirect(url_for('admin.admin_dashboard'))

# REGISTER ROUTE
@admin.route("/register")  #/admin/
def admin_register():
    if session.get('ADMIN_EMAIL'):
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/register.html')

# REGISTER HANDLER
@admin.post("/register_handle")
def register_handler():

    # Get all form input
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # Check for all input
    if not email or not name or not password:
        flash("Please fill all fields", "error")
        return redirect(url_for('admin.admin_register'))

    # Check if email already exists
    query = "SELECT * FROM admin WHERE email = %s"
    db.cursor.execute(query, [email])
    admin = db.cursor.fetchone()
    if admin:
        flash("Email already exists", "error")
        return redirect(url_for('admin.admin_register'))

    # Hash Password 
    hash_password = generate_password_hash(password)

    # Add the records to DB
    sql = "INSERT INTO admin(name, email, password) VALUES(%s, %s, %s)"
    db.cursor.execute(sql, (name, email, hash_password))
    db.conn.commit()

    if db.cursor.rowcount:
        flash("Registeration successful!", "success")
        return redirect(url_for("admin.admin_login"))
    else:
        flash("Registeration failed!", "error")
        return redirect(url_for("admin.admin_register"))


# ADMIN DASHBOARD
@admin.route("/dashboard")
@utils.is_authenticated
def admin_dashboard(): 
    email = session.get("ADMIN_EMAIL")
    sql = "SELECT name, email FROM admin WHERE email = %s"
    db.cursor.execute(sql, [email])
    admin = db.cursor.fetchone()

    return render_template("admin/dashboard.html", admin=admin)
# is_authenticated(admin_dashboard)()

# ADMIN LOGOUT
@admin.route("/logout")
def admin_logout():
    # Remove the login session [ADMIN_EMAIL]
    session.pop("ADMIN_EMAIL", None)

    # Redirect to login page 
    return redirect(url_for('admin.admin_login'))


# CATEGORY ROUTES
@admin.route('/category')
@utils.is_authenticated
def admin_category():
    # Get the logged admin
    email = session.get("ADMIN_EMAIL")
    sql = "SELECT name, email FROM admin WHERE email = %s"
    db.cursor.execute(sql, [email])
    admin = db.cursor.fetchone()

    # Get all the categories
    query = "SELECT * FROM category"
    db.cursor.execute(query)
    categories = db.cursor.fetchall()

    for x in range(len(categories)):
        categories[x]["index"] = x + 1

    return render_template(
        "admin/category.html", 
        admin=admin, 
        categories=categories, 
        len=len,
        str=str
    )


@admin.post("/category/create")
@utils.is_authenticated
def admin_category_handler():
    category_value = request.form.get("category")

    # Check if category_value has a value
    if not category_value:
        flash("Please enter a category", "error")
        return redirect(url_for("admin.admin_category"))

    # Add to DB 
    sql = "INSERT INTO category(category_name) VALUES (%s)"
    db.cursor.execute(sql, [category_value])
    db.conn.commit()

    # check if it was added to the db successfully and return the page
    if db.cursor.rowcount:
        flash("Category added successfully", "success")
    else:
        flash("Failed to add category", "error")

    return redirect(url_for("admin.admin_category")) 


# edit category
@admin.post("/category/edit")
def admin_edit_category():
    id = request.form.get("id")
    category = request.form.get("category")
    
    # SQL query
    sql = "update category set category_name = %(cat)s where category_id = %(id)s"
    db.cursor.execute(sql, { "cat": category, "id": id }) 
    db.conn.commit()

    if db.cursor.rowcount:
        flash("Category updated successfully!!!", "success")
    else:
        flash("Failed to update category", "error")
    return redirect(url_for('admin.admin_category'))


# DELETE CATEGORY
@admin.route("/category/delete/<id>")
def admin_delete_category(id):

    # SQL STATEMENT TO DELETE THE CATEGORY
    sql = "DELETE FROM category WHERE category_id = %s"
    db.cursor.execute(sql, [id])
    db.conn.commit()

    if db.cursor.rowcount:
        flash("Category deleted successfully", "success")
    else:
        flash("Failed to delete category", "error")
    
    return redirect(url_for("admin.admin_category"))


# PRODUCT ROUTES
@admin.route('/product')
@utils.is_authenticated
def admin_product():
    # Get the logged admin
    email = session.get("ADMIN_EMAIL")
    sql = "SELECT name, email FROM admin WHERE email = %s"
    db.cursor.execute(sql, [email])
    admin = db.cursor.fetchone()

    # Get all the products from the product table
    query = "SELECT * FROM product"
    db.cursor.execute(query)
    products = db.cursor.fetchall()
    # this returns a list of all the products, each in a dict of the fields(as the key) and the
    # answer to the field(as the value)

    for x in range(len(products)):
        products[x]["index"] = x + 1

    return render_template(
        "admin/product.html", 
        admin=admin, 
        products=products, 
        len=len,
        str=str
    )
    
# Product handler route
@admin.post('/product/add-product')
@utils.is_authenticated
def admin_product_handler():

    # Get all the inputs
    product_id = request.form.get("product_id")
    title = request.form.get("title")
    category = request.form.get("category")
    image = request.form.get("image")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    price = request.form.get("price")

    # Check if all inputs have a value
    if not product_id or not title or not category or not image or not description or not quantity or not price:
        flash("Please fill all fields", "error")
        return redirect(url_for("admin.admin_product"))
    
    # Add the inputs to the DB 
    sql = "INSERT INTO product(product_id, title, description, category, image, price, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    db.cursor.execute(sql, [product_id, title, description, category, image, price, quantity])
    db.conn.commit()

    # check if it was added to the db successfully and return the page
    if db.cursor.rowcount:
        flash("Product added successfully", "success")
    else:
        flash("Failed to add product", "error")

    return redirect(url_for("admin.admin_product"))


# edit and save product
@admin.post("/product/edit/<id>")
def admin_edit_product(id):

    # get all your inputs and save them in a variable
    product_id = request.form.get("product_id")
    title = request.form.get("title")
    category = request.form.get("category")
    image = request.form.get("image")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    price = request.form.get("price")
    
    # SQL query to update the new info in the db
    sql = "update product set product_id = %s, title = %s, category = %s, image = %s, description = %s, quantity = %s, price = %s where product_id = %s"
    db.cursor.execute(sql, [product_id, title, category, image, description, quantity, price, id])
    db.conn.commit()

    if db.cursor.rowcount:
        flash("Product updated successfully!!!", "success")
    else:
        flash("Failed to update product", "error")
    return redirect(url_for('admin.admin_product'))


# DELETE CATEGORY
@admin.route("/product/delete/<id>")
def admin_delete_product(id):

    # SQL STATEMENT TO DELETE THE PRODUCT
    sql = "DELETE FROM product WHERE product_id = %s"
    db.cursor.execute(sql, [id])
    db.conn.commit()

    if db.cursor.rowcount:
        flash("Product deleted successfully", "success")
    else:
        flash("Failed to delete delete", "error")
    
    return redirect(url_for("admin.admin_product"))


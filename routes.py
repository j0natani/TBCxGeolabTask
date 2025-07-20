from flask import render_template, flash
from forms import ProductForm, RegisterForm, LoginForm
from models import Product, User
import os
from ext import app, db
from flask import render_template, redirect, url_for , session
from flask_login import login_user,current_user,logout_user, login_required




@app.route("/")
def home():
    product = Product.query.all()
    return render_template("aplikacia.html", produktebi=product, role="Admin")

@app.route("/create_products", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data
        )

        image = form.img.data
        image_folder = os.path.join(app.root_path, "static", "images")
        os.makedirs(image_folder, exist_ok=True)
        directory = os.path.join(image_folder, image.filename)
        image.save(directory)

        new_product.img = image.filename
        db.session.add(new_product)
        db.session.commit()
    return render_template("create_product.html", form=form)

@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("home"))
    


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
     new_user = User(username=form.username.data, password=form.password.data)
    
     db.session.add(new_user)
     db.session.commit()
     flash("თქვენ წარმატებით დარეგისტრირდით!")
     return redirect("/login")
     

    print(form.errors)
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart=cart_items)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("detailed.html", product=product)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    from models import Product

    if 'cart' not in session:
        session['cart'] = []

    product = Product.query.get_or_404(product_id)

    for item in session['cart']:
        if item['id'] == product.id:
            item['quantity'] += 1
            break
    else:
        session['cart'].append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.img,
            'quantity': 1
        })

    session.modified = True
    return redirect("/cart")

@app.route("/product/<int:product_id>")
def products(product_id):
    detailed_product = Product.query.get(product_id)
    return render_template("detailed.html", product=detailed_product)

@app.route("/remove/<int:item_id>")
def remove_from_cart(item_id):
    cart = session.get("cart", [])

    cart = [item for item in cart if item["id"] != item_id]

    session["cart"] = cart

    return redirect(url_for("cart"))

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name , price=product.price)
  
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("create_product.html", form=form)   



from flask import redirect, url_for

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია")
            return redirect(url_for("home"))
        else:
            flash("Მომხმარებელი ან პაროლი არასწორია", "danger")
    return render_template("login.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

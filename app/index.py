import math

from flask import render_template, request, redirect, jsonify, session
# from app import app
import dao, utils
from app import app, login
from flask_login import login_user, logout_user
from app.models import UserRole


@app.route("/")
def index():
    cates = dao.load_categories()
    cate_id = request.args.get("cate_id")
    kw = request.args.get("kw")
    page = request.args.get('page', 1)
    product = dao.load_product(cate_id=cate_id, kw=kw, page=int(page))
    page_size = app.config["PAGE_SIZE"]
    total_product= dao.count_product()
    pages = math.ceil(total_product/page_size)
    return render_template("index.html", product=product, total_page=pages)


#login
@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            next = request.args.get("next")
            return redirect(next if next else "/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")



@app.route("/api/cart", methods=["post"])
def add_to_cart():

    """
    {
        "1": {
            "id": 1,
            "name": "ABC",
            "price": 123
            "quantity": 1  // default = 1
        },
        "2": {
            "id": 2,
            "name": "DEF",
            "price": 456
            "quantity": 1  // default = 1
        }
    }
    :return:
    """
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get("id"))
    name = request.json.get("name")
    price = request.json.get("price")

    if id in cart:
        cart[id]['quantity'] +=1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart
    print(cart)

    return jsonify(utils.stats_cart(cart))


@app.route("/login-admin", methods=['post'])
def login_admin_process():
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
        if user:
            login_user(user)
        return redirect("/admin")


@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.context_processor
def conmon_response():
    return {
        "category": dao.load_categories(),
        "cart_stats": utils.stats_cart(session.get("cart"))
    }


@app.route("/api/carts/<product_id>", methods=["put"])
def update_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        quantity =  int(request.json.get("quantity"))
        cart[product_id]["quantity"] = quantity

    session['cart'] = cart
    return jsonify(utils.stats_cart(cart))


@app.route("/api/carts/<product_id>", methods=["delete"])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(utils.stats_cart(cart))


@app.route("/api/pay", methods=["POST"])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({"status": 500})
    else:
        del session['cart']
        return jsonify({"status": 200})


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    with app.app_context():
        from app import admin
        app.run(debug=True)
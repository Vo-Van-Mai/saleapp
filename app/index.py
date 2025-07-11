import math

from flask import render_template, request, redirect, jsonify, session
# from app import app
import dao, utils
from app import app, login
from flask_login import login_user, logout_user


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
    return render_template("index.html", category=cates, product=product, total_page=pages)


#login
@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect("/")
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


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    with app.app_context():
        from app import admin
        app.run(debug=True)
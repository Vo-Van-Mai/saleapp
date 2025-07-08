import math

from flask import render_template, request, redirect
# from app import app
import dao
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


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(debug=True)
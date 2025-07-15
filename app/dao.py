from flask_login import current_user

from app.models import Category, Product, User, UserRole, Receipt, ReceiptDetail
from app import app, db
import hashlib


def load_categories():
    return Category.query.order_by("id").all()

def load_product(cate_id=None, kw=None, page=None):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id==cate_id)
    page_size = app.config["PAGE_SIZE"]

    if page:
        start = (page-1)*page_size
        query = query.slice(start, start+page_size)
    return query.all()

def count_product():
    return Product.query.count()

def get_user_by_id(id):
    return User.query.get(id)

def auth_user(username, password, role=None):
    password=str(hashlib.md5("123456".encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(UserRole.ADMIN))

    return u.first()

def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetail(quantity=c["quantity"], unit_price=c["price"], receipt=r, product_id=c["id"])
            db.session.add(d)

        db.session.commit()


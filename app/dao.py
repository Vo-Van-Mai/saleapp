from app.models import Category, Product, User
from app import app
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

def auth_user(username, password):
    password=str(hashlib.md5("123456".encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()
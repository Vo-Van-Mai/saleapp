import hashlib

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False, default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.USER)

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    brand = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    rating = Column(Float, default=0)
    stock = Column(Integer, default=0)
    images = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        import hashlib
        u = User(name="admin", username="admin", password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()), user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()
        # c1 = Category(name="Moble")
        # c2 = Category(name="Tablet")
        # c3 = Category(name="laptop")
        #
        # db.session.add_all([c1,c2,c3])
        # db.session.commit()

        # prod = [
        #     {
        #         "id": 1,
        #         "name": "iPhone 15 Pro Max",
        #         "category_id": 1,
        #         "brand": "Apple",
        #         "price": 33990000,
        #         "rating": 4.8,
        #         "stock": 25,
        #         "images": [
        #             "https://example.com/images/iphone15promax-front.jpg"                ]
        #     },
        #     {
        #         "id": 2,
        #         "name": "Samsung Galaxy S24 Ultra",
        #         "category_id": 1,
        #         "brand": "Samsung",
        #         "price": 29990000,
        #         "rating": 4.7,
        #         "stock": 40,
        #         "images": [
        #             "https://example.com/images/s24ultra-front.jpg"                ]
        #     },
        #     {
        #         "id": 3,
        #         "name": "MacBook Pro 14 M3",
        #         "category_id": 3,
        #         "brand": "Apple",
        #         "price": 49990000,
        #         "rating": 4.9,
        #         "stock": 15,
        #         "images": [
        #             "https://example.com/images/macbookpro14.jpg"
        #         ]
        #     },
        #     {
        #         "id": 4,
        #         "name": "Dell XPS 13 Plus",
        #         "category_id": 3,
        #         "brand": "Dell",
        #         "price": 36990000,
        #         "rating": 4.6,
        #         "stock": 20,
        #         "images": [
        #             "https://example.com/images/xps13plus.jpg"
        #         ]
        #     },
        #     {
        #         "id": 5,
        #         "name": "iPad Pro M4 12.9 inch",
        #         "category_id": 2,
        #         "brand": "Apple",
        #         "price": 35990000,
        #         "rating": 4.8,
        #         "stock": 30,
        #         "images": [
        #             "https://example.com/images/ipadpro2024.jpg"
        #         ]
        #     },
        #     {
        #         "id": 6,
        #         "name": "Samsung Galaxy Tab S9 Ultra",
        #         "category_id": 2,
        #         "brand": "Samsung",
        #         "price": 29990000,
        #         "rating": 4.5,
        #         "stock": 35,
        #         "images": [
        #             "https://example.com/images/tabs9ultra.jpg"
        #         ]
        #     }
        # ]
        #
        # for p in prod:
        #     product = Product(**p)
        #     db.session.add(product)
        #
        # db.session.commit()


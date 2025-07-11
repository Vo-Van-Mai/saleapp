from app.models import Category, Product, User
from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name="E-Commerce Admin", template_mode="bootstrap4")

class CategoryView(ModelView):
    column_list = ['name', 'products']

class ProductModelView(ModelView):
    column_list = ["id", "name", "price"]
    can_export = True
    column_filters = ["id", "name", "price"]
    column_searchable_list = ['name']
    page_size = 4
    column_editable_list = ['name']


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))

from app.models import Category, Product, User, UserRole
from app import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect

admin = Admin(app=app, name="E-Commerce Admin", template_mode="bootstrap4")

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class CategoryView(AdminView):
    column_list = ['name', 'products']

class ProductModelView(AdminView):
    column_list = ["id", "name", "price"]
    can_export = True
    column_filters = ["id", "name", "price"]
    column_searchable_list = ['name']
    page_size = 4
    column_editable_list = ['name']


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(AuthenticatedView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")



class StatsView(AuthenticatedView):
    @expose("/")
    def index(self):
        return self.render("/admin/stats.html")




admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductModelView(Product, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(StatsView(name="Thống kê"))

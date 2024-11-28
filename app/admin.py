from flask import redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user

from app import db, app
from app.models import User, UserRole


class LoginRequired(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AboutUsView(LoginRequired):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


class LogoutView(LoginRequired):
    @expose("/")
    def logout_view(self):
        logout_user()
        return redirect("/admin")


class StatsView(LoginRequired):
    @expose("/")
    def stats_view(self):
        return self.render("admin/stats.html")


class LoginRequiredView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.QUAN_LY)


class UserView(LoginRequiredView):
    column_searchable_list = ['username']
    column_filters = ['id', 'username']
    can_view_details = True


admin = Admin(app, name='test', template_mode='bootstrap4')
admin.add_view(AboutUsView(name="Giới thiệu"))
admin.add_view(UserView(User, db.session, name="Người dùng"))
admin.add_view(StatsView(name="Thống kê"))
admin.add_view(LogoutView(name="Đăng xuất"))

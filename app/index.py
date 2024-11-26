from flask import render_template, request, redirect, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app import app, login
from app.dao import UserDAO
from app.model import User, UserRole


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_portal")
@login_required
def admin_view():
    return render_template("admin_portal/dashboard.html")

@app.route("/redirect")
def redirect_user():
    if current_user.user_role == UserRole.QUAN_LY:
        return redirect("/admin_portal")
    if current_user.user_role == UserRole.NHAN_VIEN:
        return redirect("/employee_portal")
    return redirect("/")

@app.route("/employee_portal")
@login_required
def e_view():
    return render_template("employee_portal/index.html")


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        remember = "remember_me" in request.form

        user = User.query.filter(User.username == username).first()

        if user and user.check_password(password):
            login_user(user=user, remember=remember)
            return redirect("/redirect")
        flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
        return redirect("/login")
    if current_user.is_authenticated:
        return redirect("/redirect")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/check-availability/<username>")
def check_for_availability(username):
    if UserDAO.user_exist(username):
        return jsonify({"available": False})
    else:
        return jsonify({"available": True})


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        print(f"POST Data: {request.form}")
        username = request.form.get("username")
        if UserDAO.user_exist(username=username):
            flash("Tên người dùng không còn khả dụng!","danger")
            return redirect("/register")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        name = first_name + " " + last_name
        email = request.form.get("email")
        # if UserDAO.user_exist(email=email):
        #     flash("Địa chỉ email đã được sử dụng để đăng ký", "danger")
        #     return redirect("/register")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        UserDAO.create_user(name=name, username=username, password=password,role=UserRole.KHACH_HANG)
        flash("Tài khoản đã được tạo thành công!", "danger")
        return redirect("/login")
    if current_user.is_authenticated:
        return redirect("/")
    return render_template("register.html")

@app.route("/profile", methods=["POST", "GET"])
@login_required
def update_account_view():
    return render_template("update-account.html")

@app.route("/profile/change_password", methods=["POST","GET"])
@login_required
def change_password_view():
    return render_template("change-password.html")


if __name__ == "__main__":
    app.run(debug=True)

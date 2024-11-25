from flask import render_template, request, redirect, flash, jsonify
from flask_login import login_user, logout_user

from app import app, login
from app.dao import UserDAO
from app.model import User, UserRole


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_portal")
def admin_view():
    return render_template("index.html")


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# đang làm login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = "remember_me" in request.form

        user = User.query.filter(User.username == username).first()

        if user and user.check_password(password):
            login_user(user=user, remember=remember)
            if user.user_role == UserRole.QUAN_LY:
                return redirect("/admin_portal")
            if user.user_role == UserRole.NHAN_VIEN:
                return redirect("/e")
            return redirect("/")
        flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
        return redirect("/login")
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
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)

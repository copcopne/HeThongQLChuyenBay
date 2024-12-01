from flask import render_template, request, redirect, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app import app, login, utils
from app.dao import UserDAO
from app.models import User, UserRole


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/redirect")
def redirect_user():
    if current_user.user_role == UserRole.QUAN_LY:
        return redirect("/admin")

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

        if UserDAO.auth_user(username=username, password=password):
            login_user(user=user, remember=remember)
            return redirect("/")

        flash(message="Sai tên đăng nhập hoặc mật khẩu!",category="danger")
        return redirect("/login")

    if current_user.is_authenticated:
        return redirect("/")

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

        username = request.form.get("username")

        if UserDAO.user_exist(username=username):
            flash("Tên người dùng không còn khả dụng!", "danger")
            return redirect("/register")

        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        name = first_name + " " + last_name
        email = request.form.get("email")

        if UserDAO.user_exist(email=email):
            flash("Địa chỉ email đã được sử dụng để đăng ký", "danger")
            return redirect("/register")

        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        UserDAO.create_user(name=name, username=username, password=password, email=email, role=UserRole.KHACH_HANG)

        flash("Tài khoản đã được tạo thành công!", "success")

        return redirect("/login")

    if current_user.is_authenticated:
        return redirect("/")

    return render_template("register.html")


@app.route("/profile", methods=["POST", "GET"])
@login_required
def update_account_view():
    return render_template("update-info.html")


@app.route("/profile/change_basic_info", methods=["POST", "GET"])
def update_profile():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("emailAddress")

        msg = UserDAO.update_profile(user=current_user, first_name=first_name,
                                     last_name=last_name, username=username, email=email)

        flash(message=msg, category=utils.get_flash_category(msg))

        return redirect("/profile")

    return render_template("update-info.html")


@app.route("/profile/change_basic_info/profile_picture", methods=["POST"])
def upload_profile_picture():
    profile_pic = request.files.get("profile_picture")
    msg = UserDAO.update_profile(user=current_user, profile_picture=profile_pic)

    flash(message=msg, category=utils.get_flash_category(msg))

    return redirect("/profile")


@app.route("/profile/change_password", methods=["POST", "GET"])
@login_required
def update_password():
    if request.method == "POST":

        old = request.form.get("old_password")

        if UserDAO.auth_user(username=current_user.username, password=old):
            msg = ""
            new = request.form.get("password")
            print(new)
            if new.__eq__(request.form.get("confirm_password")):
                msg = UserDAO.update_profile(user=current_user, password=new)

            flash(message=msg, category=utils.get_flash_category(msg))
            return redirect("/profile")

    return render_template("update-password.html")


@app.route("/login_as_admin", methods=["POST"])
def login_as_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    user = UserDAO.auth_user(username=username, password=password, role=UserRole.QUAN_LY)

    if user:
        login_user(user=user)

    return redirect("/admin")


@app.context_processor
def inject_user_role():
    return dict(UserRole=UserRole)


if __name__ == "__main__":
    app.run(debug=True)

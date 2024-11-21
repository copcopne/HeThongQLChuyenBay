from app import app, login_manager
from flask import render_template, request, redirect
from flask_login import login_user, logout_user
import dao, hashlib
from app.model import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login_view():
    return render_template("login.html")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
# đang làm login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(username == username, str(hashlib.md5(password.encode("utf-8")).hexdigest()) == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin_portal")


if __name__ == "__main__":
    app.run(debug=True)
import cloudinary.uploader
from cloudinary.exceptions import Error

from app.models import User, db


class UserDAO:
    @staticmethod
    def get_user_by_id(user_id):

        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):

        return User.query.filter(username == username).first()

    @staticmethod
    def create_user(name, username, password, email, role):

        new = User(username=username, user_role=role, email=email,
                   profile_picture="https://www.gravatar.com/avatar/?d=mp")
        new.set_password(password)

        db.session.add(new)
        db.session.commit()
        return new

    @staticmethod
    def user_exist(username=None, email=None):

        if username:
            return User.query.filter(User.username == username).first() is not None

        if email:
            return User.query.filter(User.email == email).first() is not None
        return False

    @staticmethod
    def auth_user(username, password, role=None):
        print(f"Password: {password}")
        _user = User.query.filter(User.username.__eq__(username)).first()
        if _user and _user.check_password(password) and (role is None or _user.user_role == role):
            return _user

        return None

    @staticmethod
    def update_profile(user, username=None, password=None, first_name=None, last_name=None, email=None,
                       profile_picture=None):
        response = ""
        _user = User.query.filter(User.username == user.username).first()
        if profile_picture:
            try:
                res = cloudinary.uploader.upload(profile_picture)
                _user.profile_picture = res.get("secure_url")
                db.session.commit()
                response = "Tải lên thành công!"

            except Error as e:
                response = "LỖI khi tải ảnh lên: " + str(e)
        else:
            if username:
                _user.username = username
            if email:
                _user.email = email
            if first_name:
                pass
            if last_name:
                pass
            if password:
                _user.set_password(password)

            db.session.commit()

            response = "Cập nhật thông tin thành công!"

        return response

from app.model import User, db


class UserDAO:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter(username == username).first()

    @staticmethod
    def create_user(name, username, password, role):
        new = User(name=name, username=username, user_role=role)
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
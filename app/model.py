from enum import Enum as RoleEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Enum
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, app


class UserRole(RoleEnum):
    QUAN_LY = 1,
    NHAN_VIEN = 2,
    KHACH_HANG = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.KHACH_HANG)

    def set_password(self, p_password):
        self.password = generate_password_hash(p_password)

    def check_password(self, p_password):
        return check_password_hash(self.password, p_password)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin = User(name="admin", username="admin", user_role=UserRole.QUAN_LY)
        admin.set_password("123456")

        db.session.add(admin)
        db.session.commit()

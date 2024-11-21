from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
import hashlib

class UserRole(RoleEnum):
    ADMIN = 1,
    USER = 2

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin = User(name="admin", username="admin", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                     user_role=UserRole.ADMIN)

        db.session.add(admin)
        db.session.commit()
from urllib.parse import quote

import cloudinary
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/flightdb?charset=utf8mb4" % quote(
    'Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "DSJKHFSDLKFSDfSIXNDFSAHJF@#243294@!"
db = SQLAlchemy(app)
login = LoginManager(app)
login_manager = LoginManager()

cloudinary.config(
    cloud_name="dq3dtj8lz",
    api_key="582527119715667",
    api_secret="zWDS8SbqF_hr_aDUMyS0PKiyWK8")

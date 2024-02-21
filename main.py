from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)
app.app_context().push()


# #CREATE TABLE IN DB
class Listings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100))
    rooms = db.Column(db.Integer, nullable=False)
    baths = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(250), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)


# Line below only required once, when creating DB.
# with app.app_context():
#     db.create_all()


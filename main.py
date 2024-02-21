from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, URL
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)
app.app_context().push()
Bootstrap5(app)


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


# Already created to initialize DB so we comment out
# new_listing = Listings(
#     address="Dagnall Street, SW11",
#     type="Flat",
#     rooms=2,
#     baths=12,
#     link="https://www.rightmove.co.uk/properties/86714010#/?channel=RES_LET",
#     price=2000
# )
#
# db.session.add(new_listing)
# db.session.commit()


class CreateListingForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired()])
    type = SelectField("Type", choices=[("flat", "Flat"), ("house", "House")], validators=[DataRequired()])
    rooms = IntegerField("Rooms", validators=[DataRequired()])
    baths = IntegerField("Baths", validators=[DataRequired()])
    link = StringField("URL", validators=[DataRequired(), URL()])
    price = IntegerField("Price", validators=[DataRequired()])
    submit = SubmitField("Submit Listing")


@app.route("/")
def home():
    result = db.session.execute(db.select(Listings).order_by(Listings.price))
    all_listings = result.scalars().all()
    return render_template("index.html", listings=all_listings)


@app.route("/add", methods=["GET", "POST"])
def add_listing():
    form = CreateListingForm()
    if form.validate_on_submit():
        listing = Listings(
            address=form.address.data,
            type=form.type.data,
            rooms=form.rooms.data,
            baths=form.baths.data,
            link=form.link.data,
            price=form.price.data)
        db.session.add(listing)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5005)
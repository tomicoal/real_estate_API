import os

import flask
from flask import Flask, render_template, url_for, redirect
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask.json import jsonify


UPLOAD_FOLDER = 'static/assets/img/house_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)

# #CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listings.db'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


# #CREATE TABLE IN DB
class Listings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100))
    rooms = db.Column(db.Integer, nullable=False)
    baths = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String, nullable=False)


# Line below only required once, when creating DB.
with app.app_context():
    db.create_all()


class CreateListingForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired()])
    type = SelectField("Type", choices=[("flat", "Flat"), ("house", "House")], validators=[DataRequired()])
    rooms = IntegerField("Rooms", validators=[DataRequired()])
    baths = IntegerField("Baths", validators=[DataRequired()])
    description = CKEditorField("Listing description", validators=[DataRequired()])
    link = StringField("URL", validators=[DataRequired(), URL()])
    price = IntegerField("Price", validators=[DataRequired()])
    image = FileField("Image", validators=[DataRequired()])
    submit = SubmitField("Submit Listing")


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def get_all_listings():
    results = db.session.execute(db.select(Listings))
    listings = results.scalars().all()
    return render_template("index.html", all_listings=listings)


@app.route("/add", methods=["GET", "POST"])
def add_listing():
    form = CreateListingForm()
    if form.validate_on_submit():

        image_file=form.image.data

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        listing = Listings(
            address=form.address.data,
            type=form.type.data,
            rooms=form.rooms.data,
            baths=form.baths.data,
            description=form.description.data,
            link=form.link.data,
            price=form.price.data,
            image_url=f"../static/assets/img/house_images/{image_file.filename}")
        db.session.add(listing)
        db.session.commit()

        return redirect(url_for('get_all_listings'))
    return render_template("add.html", form=form)


@app.route("/listing/<int:listing_id>")
def show_listing(listing_id):
    requested_listing = db.get_or_404(Listings, listing_id)
    return render_template("listing.html", listing=requested_listing)


if __name__ == '__main__':
    app.run(debug=True, port=5005)

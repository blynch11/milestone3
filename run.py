import os
import json
from flask import (
    Flask, render_template, request, flash, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html", page_title="register")


@app.route("/beers")
def beers():
    reviews = mongo.db.Reviews.find()
    return render_template("beers.html", reviews = reviews, page_title="beers")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we received your message!".format(request.form.get("name")))
    return render_template("contact.html", page_title="contact")


@app.route("/login")
def login():
    return render_template("login.html", page_title="login")


@app.route("/breweries")
def breweries():
    data = []
    with open("data/breweries.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("breweries.html", page_title="breweries", breweries=data)




if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
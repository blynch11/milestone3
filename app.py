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


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    reviews = mongo.db.reviews.find({"$text": {"$search": query}})
    return render_template("user_reviews.html", reviews=reviews)


@app.route("/login", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username exists already
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("username already exists")
            return redirect(url_for("login"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        #put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
    return render_template("login.html", page_title="register")


@app.route("/user_reviews", methods=["GET", "POST"])
def user_reviews():
    if request.method == "POST":

        reviews = mongo.db.reviews.find()
        # get users reviews and add their key values to DB
        user_reviews = {
                "beer_name": request.form.get("beer_name"),
                "beer_style": request.form.get("beer_style"),
                "beer_review": request.form.get("beer_review"),

            }
        mongo.db.reviews.insert_one(user_reviews)

        session["reviews"] = request.form.get("beer_name")
        session["reviews"] = request.form.get("beer_style")
        session["reviews"] = request.form.get("beer_review")
        return redirect(index)

    reviews = mongo.db.reviews.find()
    return render_template("user_reviews.html", reviews=reviews)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we received your message!".format(request.form.get("name")))
    return render_template("contact.html", page_title="contact")


@app.route("/login",  methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # See if user name already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
                # ensure the hashed password is a match
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("welcome, {}".format(request.form.get("username")))
                    
            else:
                # password doesn't match
                flash("incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
                # Username entered does not exist
            flash("Incorrect Username and/or Password ")
            return redirect(url_for("login"))

    return render_template("login.html", page_title="login")


@app.route("/breweries")
def breweries():
    data = []
    with open("data/breweries.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("breweries.html", 
        page_title="breweries", breweries=data)



if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
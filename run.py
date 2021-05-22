import os
import json
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/beers")
def beers():
    return render_template("beers.html", page_title="beers")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we received your message!".format(request.form.get("name")))
    return render_template("contact.html", page_title="contact")


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
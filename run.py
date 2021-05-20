import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/beers")
def beers():
    return render_template("beers.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/breweries")
def breweries():
    return render_template("breweries.html")




if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars_1
import os

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection locally
mongo = PyMongo(app, uri="mongodb://localhost:8888/mars_app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scraper functions
    mars_info = scrape_mars_1.scrape_mars_info()

    #Update Mongo database
    mongo.db.collection.update({}, mars_info, upsert=True)

    #return redirect
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
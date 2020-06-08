from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

#Spin up the Flask App
app = Flask(__name__, template_folder='templates')


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Or set inline
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Creation of connection variable. Connection to local host for local Mongo. 
#conn = "mongodb://localhost:27017"

#Pass connection to the pymongo instance"
#client = pymongo.MongoClient(conn)

#Connect to a database. Will create one if not already available
#db = client.redplanet_db
#mars = db.mars_dict

#Drops collection if available to remove dublicates
#db.mars_dict.drop()

#Mongo Creates Collection automatically
#db.mars_dict.inset_many()#insert list of dict

#App Route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", data=mars)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    #Redirect to the homepage
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
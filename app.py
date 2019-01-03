# Import Flask
from flask import Flask, render_template, redirect
# Import pymongo
from flask_pymongo import PyMongo

# Importing python file that has scrape() function defined
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Creating flask-Mongodb connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

@app.route("/scrape")

def scrape():
    
    scraped_data = mongo.db.scraped_data
    mars_data = scrape_mars.scrape()
    scraped_data.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

@app.route("/")

def query():
    # Return a single document from the scraped_data collection saved in mission_to_mars db and store it in mars_data variable
    mars_data = mongo.db.scraped_data.find_one()
    # pass the mars_data into an HTML template to display the data
    return render_template("index.html", mars_data = mars_data)
    

if __name__ == "__main__":
    app.run(debug=True)

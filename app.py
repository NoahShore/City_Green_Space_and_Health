#Import dependencies
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import numpy as np


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/green_spaces_and_health3"

mongo = PyMongo(app)

#Define static routes. Define what to do when a user hits the index route
#################################################
# Flask Routes
#################################################
#each page of website needs its own app.route
# Add function below it. 
@app.route("/")
def welcome():
    author = "gabriella, kent, noah, naseema"
    """List all available api routes."""
    return render_template('home.html', author=author)
            # f"Available Routes:<br/>"
            # f"map<br/>"
            # f"dropdown"
            # f"barcharts"
            # f"bubblechart"
            # f"TopTenCharts"
        
# Route to get data from MongoDB
#################################################
# Database Setup
#################################################

@app.route("/mongo")
def readMongo():
    data = mongo.db.green_spaces_and_health3.find({}, {'_id': 0, 'city': 1, 'state': 1, 'park_acres': 1,
                                            'percent_of_city_area': 1, 'dv_data_value': 1, 'ob_data_value': 1, 
                                            'mh_data_value': 1, 'lat': 1, 'lon': 1})
    result = []
    for x in data:
        result.append(x)
    print(jsonify(result))
    return jsonify(result)

# Visualization: Map
@app.route("/map")
def map():

    return render_template('map.html')


# Dropdown Menu 
@app.route("/dropdown")



#return render_template('index.html')

# Visualization: Bar Charts
@app.route("/bar_chart")
def bar_chart():
    city_data = mongo.db.green_spaces_and_health3.find({}, {'_id': 0, 'cities': 1, 'state': 1, 'park_acres':1})
    result = city_data
    return render_template('bar_chart.html', result=result)

#Visualization Bubble Charts
@app.route("/scatter_plot")
def bubble_chart():
    bub_data = mongo.db.green_spaces_and_health3.find(
        {}, {'_id': 0, 'cities': 1, 'state': 1, 'ob_data_value': 1})
    result = bub_data
    return render_template('scatter_plot.html', result=result)

# Third visualization page - pie charts
@app.route("/line_column")
def line_column():
    line_data = mongo.db.green_spaces_and_health3.find(
        {}, {'_id': 0, 'cities': 1, 'state': 1, 'ob_data_value': 1})
    result = line_data
    return render_template('line_column.html', result=result)

## LEAVE THIS IN HERE these are the very last 2 lines
# End Flask 
if __name__ == "__main__":
    app.run(debug=True)


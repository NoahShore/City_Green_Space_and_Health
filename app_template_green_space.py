#DRAFT TEMPLATE from 10.3 flask activities EXAMPLES

# 1. import Flask
from flask import Flask
# or more applicable imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Passenger = Base.classes.passenger


# Create an app, being sure to pass __name__
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Create a dictionary to hold a key, value pair.
hello_dict = {"Hello": "World!"}

# 3. Define static routes. Define what to do when a user hits the index route
#################################################
# Flask Routes
#################################################
@app.route("/")#DEFINES HOMEPAGE
def index():
    return render_template('index.html')
# or
def welcome():
    """List all available api routes."""
    return (
         f"Welcome to the Justice League API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/justice-league<br/>"
        f"/api/v1.0/justice-league/superhero/batman<br/>"
        f"/api/v1.0/justice-league/real_name/bruce%20wayne"
    )
# @app.route("/about")
# def about():

@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)
#or
@app.route("/about")
def about():
    name = "Peleke"
    location = "Tien Shan"

    return f"My name is {name}, and I live in {location}."
# or
@app.route("/api/v1.0/justice-league/<real_name>")
def justice_league_character(real_name):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = real_name.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404

@app.route("/api/v1.0/justice-league/superhero/<superhero>")
def justice_league_by_superhero__name(superhero):
    """Fetch the Justice League character whose superhero matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = superhero.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["superhero"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": "Character not found."}), 404

@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


@app.route("/contact")
def contact():
    email = "peleke@example.com"

    return f"Questions? Comments? Complaints? Shoot an email to {email}."

# 4. Define what to do when a user hits the /about route.  print only appears for us in the termina, the return appears for the user.
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

#NEEDS TO BE THE LAST LINE OF THE PROGRAM
if __name__ == "__main__":
    app.run(debug=True)
# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data from the last year."""
    # Perform a query to retrieve the data and precipitation scores
    precip_data_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= dt.date(2017, 8, 23)).\
        filter(Measurement.date >= dt.date(2016, 8, 23)).\
        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert query results into a dictionary
    precipitation = []
    for date, prcp in precip_data_query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    stations_query = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations_query))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the last year of temperature data for the most active station."""
    # Query the last year of temperature data
    temp_data_query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date <= dt.date(2017, 8, 23)).\
    filter(Measurement.date >= dt.date(2016, 8, 23)).\
    order_by(Measurement.tobs).all()

    session.close()

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(temp_data_query))

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def temp_from(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Fetch the minimum, maximum and average temperature from the specified start
    date to the end of the data set."""
    #Query the min, max and avg
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    temp_stats_list = list(np.ravel(temp_stats))

    return jsonify(temp_stats_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_from(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Fetch the minimum, maximum and average temperature from the specified start
    date to the specified end date."""
    #Query the min, max and avg
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    temp_stats_list = list(np.ravel(temp_stats))

    return jsonify(temp_stats_list)
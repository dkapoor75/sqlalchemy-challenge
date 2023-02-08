import numpy as np

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

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # fetch data of teh last year from the database
    year_str = "2017"
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).filter(func.strftime("%Y", Measurement.date) == year_str).all()
    
    session.close()

    # Create a dictionary to hold the data fom measurement table and return as json
    all_prcp_data = []
    for station, date, prcp in results:
        prcp_dict = {}
        prcp_dict["station"] = station
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp_data.append(prcp_dict)

    return jsonify(all_prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # fetch data of teh last year from the database
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Create a dictionary
    all_station_data = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_station_data.append(station_dict)

    return jsonify(all_station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # fetch the station that is most active
    year_str = "2017"
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(func.strftime("%Y", Measurement.date) == year_str).all()
    
    session.close()

    # Create a dictionary
    active_station_data = []
    for station, date, tobs in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["date"] = date
        station_dict["tobs"] = tobs
        active_station_data.append(station_dict)

    return jsonify(active_station_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # fetch the min, max and average temperatures of all dates higher or equal to the start date given as parameter
    results = session.query(Measurement.date, func.min(Measurement.tobs).label("min"), func.max(Measurement.tobs).label("max"), func.avg(Measurement.tobs).label("avg")).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    session.close()
    
    # Create a dictionary
    temp_data_higher_than_start_date = []
    for date, min, max, avg in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["min"] = min
        temp_dict["max"] = max
        temp_dict["avg"] = avg
        temp_data_higher_than_start_date.append(temp_dict)

    return jsonify(temp_data_higher_than_start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # fetch the min, max and average temperatures of all dates higher or equal to the start date given as parameter
    results = session.query(Measurement.date, func.min(Measurement.tobs).label("min"), func.max(Measurement.tobs).label("max"), func.avg(Measurement.tobs).label("avg")).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    
    session.close()
    
    # Create a dictionary
    temp_data_between_start_and_end = []
    for date, min, max, avg in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["min"] = min
        temp_dict["max"] = max
        temp_dict["avg"] = avg
        temp_data_between_start_and_end.append(temp_dict)

    return jsonify(temp_data_between_start_and_end)

if __name__ == '__main__':
    app.run(debug=True)
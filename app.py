# Import the dependencies.
import numpy as np

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(bind=engine)
#################################################
# Flask Setup
#################################################
app = flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return (
        f"Available Routes are:<br/>"
        f"</api/v1.0/precipitation<br/>"
        f"</api/v1.0/stations<br/>"
        f"</api/v1.0/tobs<br/>"
        f"</api/v1.0/<start><br/>"
        f"</api/v1.0/<start>/<end><br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query for precipitation last 12 months
    precipitation_data = session.query(measurement.date, func.avg(measurement.prcp)).\
                    group_by(measurement.date).all()


    #En Session
    session.close()

    #Put precipitation query into a dictionary
    precipitation_list = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_list)
    #jsonify
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def station():
    #list of all stations
    station_query = session.query(station.station, station.id).all()
#close session

    session.close()
    #Station query put into dictionary 

    station_list = []
    for station, id in station_query:
        station_dict ={}
        station_dict['station'] = station
        station_dict['id'] = id
        station_list.append(station_dict)
    #jsonify
    return jsonify (station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    #Most active station from past year

    past_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Retrieve info of most active station

    tobs_station = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                        filter(measurement.date >= past_year).all()

    #close session
    session.close()

    tobs_list = []
    for date, tobs, station in tobs_station:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["station"] = station
    tobs_list.append(tobs_dict)
    #jsonify
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):

    session.close()

@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):

    
    
#End session
    session.close()

if __name__ == '__main__':
    app.run(debug=true)


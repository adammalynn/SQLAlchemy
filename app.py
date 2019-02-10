import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation/api/v1.0/stations/api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation/api/v1.0/stations/api/v1.0/tobs/api/v1.0/start<br/>"
        f"/api/v1.0/precipitation/api/v1.0/stations/api/v1.0/tobs/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value"""
    """Return the JSON representation of your dictionary"""
    # query the 
    query_date = dt.date(2017, 8,23) -dt.timedelta(days=365)
    qry = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).group_by(Measurement.date).order_by(Measurement.date).all()

    # another method is
    # first_dict = {}
# for record in qry:
#     first_dict[record[0]] = record[1]
# print(first_dict)

    qrydict = dict(qry)
    

    return jsonify(qrydict)


@app.route("/api/v1.0/precipitation/api/v1.0/stations")
def stat():
    '''return a json list of stations'''
    results = session.query(Station.station).all()

    return jsonify(results)

@app.route("/api/v1.0/precipitation/api/v1.0/stations/api/v1.0/tobs")
def temps():
    """query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year"""
    
    qryt = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    return jsonify(qryt)

@app.route("/api/v1.0/precipitation/api/v1.0/stations/api/v1.0/tobs/api/v1.0/start")
def start():
    """query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year"""
    
    def calc_temps(start_date):
        
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()        
    start_new = calc_temps('2011-02-28')
    return jsonify(start_new)


@app.route("/api/v1.0/precipitation/api/v1.0/stations/api/v1.0/tobs/api/v1.0/start/end")
def end():
    """query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year"""
    def calc_temps(start_date, end_date):
    
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    data_t=calc_temps('2011-02-28', '2011-03-05')
    return jsonify(data_t)


if __name__ == '__main__':
    app.run(debug=True)

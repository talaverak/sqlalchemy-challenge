# Import the dependencies.
import numpy as np
from datetime import datetime as dt

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
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)
# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes

@app.route("/")
def homepage():
    return(
        f"The avaliable routes are listed below for Hawaiian Climate <br/>"       
        f"/api/v1.0/precipitation<br/>"        
        f"/api/v1.0/stations<br/>"       
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    import datetime as dt
    
    one_year_from_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    precipitation_scores = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_from_date).all()
        
    session.close()
        
    precip = {date: prcp for date, prcp in precipitation_scores}
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    
    stations = session.query(station.name, station.station).all()
    
    session.close()
    
    stations_dict = dict(stations)
    
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    
    import datetime as dt
    
    one_year_from_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    active_station_temps = session.query(measurement.date, measurement.tobs).filter(measurement.station=="USC00519281").\
        filter(measurement.date >= one_year_from_date).all()
        
    session.close()
        
    tobs_dict = dict(active_station_temps)
    
    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    
    start_date = dt.strptime(start_date,'%Y-%m-%d')
    
    trip_start = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
       filter(measurement.date >= start_date).all()
        
    results = trip_start[0]
    
    session.close()
    
    start_date_temps = []
    start_date_temps_dict = {}
    start_date_temps_dict["Min"] = results[0]
    start_date_temps_dict["Max"] = results[1]
    start_date_temps_dict["Avg"] = results[2]
    start_date_temps.append(start_date_temps_dict)
    
    return jsonify(start_date_temps)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    
    start_end_trip = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
        
    results = start_end_trip[0]
    
    session.close()
    
    start_end_trip_temps = []
    start_end_trip_temps_dict = {}
    start_end_trip_temps_dict ["Min"] = results[0]
    start_end_trip_temps_dict["Max"] = results[1]
    start_end_trip_temps_dict ["Avg"] = results[2]
    start_end_trip_temps.append(start_end_trip_temps_dict)
        
    return jsonify(start_end_trip_temps)
    
if __name__ == '__main__':
    app.run(debug=True)
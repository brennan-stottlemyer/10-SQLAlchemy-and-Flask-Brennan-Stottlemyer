import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
import time
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:////Users/bstottlemyer/BootCamp/UDEN201902DATA4/10-Adv-Data/Homework_Instructions/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/'fill_in_start_date'<br/>"
    f"/api/v1.0/'fill_in_start_date'/'fill_in_end_date'")

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation_list = (session.query(Measurement.date,Measurement.prcp)
                        .all())

    precipitation_data = []
    for record in range(len(precipitation_list)):
        precipitation_dict = {}
        precipitation_dict['date'] = precipitation_list[record][0]
        precipitation_dict['precipitation'] = precipitation_list[record][1]
        precipitation_data.append(precipitation_dict)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    station_list = (session.query(Station.station, Station.name)
                    .all())

    station_data = []
    for record in range(len(station_list)):
        station_dict = {}
        station_dict['station'] = station_list[record][0]
        station_dict['name'] = station_list[record][1]
        station_data.append(station_dict)
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    last_row = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_day_in_data = last_row.__dict__

    one_year_ago = int(last_day_in_data['date'][:4]) - 1

    full_date_one_year_ago = f"{one_year_ago}-{last_day_in_data['date'][5:7]}-{last_day_in_data['date'][8:10]}"
    
    last_12_months_precipitation_list = (session.query(Measurement.date,Measurement.tobs)
                                    .filter(Measurement.date >= full_date_one_year_ago)
                                    .all())

    one_year_temperature_data = []
    for record in range(len(last_12_months_precipitation_list)):
        temperature_dict = {}
        temperature_dict['date'] = last_12_months_precipitation_list[record][0]
        temperature_dict['temperature'] = last_12_months_precipitation_list[record][1]
        one_year_temperature_data.append(temperature_dict)
    return jsonify(one_year_temperature_data)                                

@app.route("/api/v1.0/<start>")
def temp_start(start = None):
    start_date_temperature_list = (session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
                                .filter(Measurement.date >= start)
                                .group_by(Measurement.date)
                                .all())
    
    start_date_temperature_data = []
    for record in range(len(start_date_temperature_list)):
        
        temperature_dict = {}
        temperature_dict['date'] = start_date_temperature_list[record][0]
        temperature_dict['min_temperature'] = start_date_temperature_list[record][1]
        temperature_dict['max_temperature'] = start_date_temperature_list[record][2]
        temperature_dict['avg_temperature'] = start_date_temperature_list[record][3]
        start_date_temperature_data.append(temperature_dict)
    return jsonify(start_date_temperature_data) 

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date(start = None, end = None):
    start_and_end_date_temperature_list = (session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
                .filter(Measurement.date >= start, Measurement.date <= end)
                .group_by(Measurement.date)
                .all()) 
    
    start_and_end_date_temperature_data = []
    for record in range(len(start_and_end_date_temperature_list)):
        temperature_dict = {}
        temperature_dict['date'] = start_and_end_date_temperature_list[record][0]
        temperature_dict['min_temperature'] = start_and_end_date_temperature_list[record][1]
        temperature_dict['max_temperature'] = start_and_end_date_temperature_list[record][2]
        temperature_dict['avg_temperature'] = start_and_end_date_temperature_list[record][3]
        start_and_end_date_temperature_data.append(temperature_dict)
    return jsonify(start_and_end_date_temperature_data) 

if __name__ == "__main__":
    app.run(debug=True)
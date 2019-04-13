from flask import Flask, jsonify
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Index' page...")
    return (
        f"<h3>Welcome to the HawaiiKawaii API!</h3>"
        f"<strong>Static Routes:</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"<strong>Date Routes:</strong><br/>"
        f"Use the following format for start_date and end_date: 'YYYY-MM-DD'<br/>"
        f"/api/v1.0/start_date<br/>"    
        f"/api/v1.0/start_date/end_date<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_obj = datetime.strptime(last_date[0], '%Y-%m-%d').date()
    year_ago = last_date_obj - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    prcp = dict(prcp_data)
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    ss = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    return jsonify(ss)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_obj = datetime.strptime(last_date[0], '%Y-%m-%d').date()
    year_ago = last_date_obj - dt.timedelta(days=365)
    tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    return_dict = {'Min':start[0][0],'Avg':start[0][1],'Max':start[0][2]}
    return jsonify(return_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date, end_date):
    startend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return_dict = {'Min':startend[0][0],'Avg':startend[0][1],'Max':startend[0][2]}
    return jsonify(return_dict)

if __name__ == "__main__":
    app.run(debug=True)
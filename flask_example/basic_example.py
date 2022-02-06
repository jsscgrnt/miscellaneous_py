import requests
import pandas as pd
from distutils.log import debug
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

__author__ = 'jessica'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    lat = request.form['lat']
    long = request.form['long']
    source = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={long}"
    page = requests.get(source)
    soup = BeautifulSoup(page.content, 'html.parser')
    seven_day = soup.find(id="seven-day-forecast")
    periods = [pt.get_text() for pt in seven_day.select(".tombstone-container .period-name")]
    short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
    temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
    descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

    weather = pd.DataFrame({
        "Period": periods,
        "Short description": short_descs,
        "Temperature": temps,
        "Long description": descs
    })

    return(f'<h3> Your summarized forecast is: </h3> {weather.to_html(header="true", table_id="table")} <br/> <b> Source: </b> {source} <br/> <br/><a href="/">Back Home</a>')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3022, debug = True)
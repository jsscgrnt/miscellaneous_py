__author__ = 'jessica'

import requests
import folium
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/map')
def map():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    folium_map.add_child(folium.LatLngPopup())
    return folium_map._repr_html_()

@app.route('/forecast', methods=['POST'])
def forecast():
    lat = request.form['lat']
    long = request.form['long']

    page = requests.get(f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={long}")
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

    return 'Hi, your summarized forecast is: %s <br/> <a href="/">Back Home</a>' % (weather.to_html(header="true", table_id="table")
)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host = '0.0.0.0', port = 3009)
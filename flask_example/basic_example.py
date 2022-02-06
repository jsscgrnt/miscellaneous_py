__author__ = 'jessica'
from distutils.log import debug
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    lat = request.form['lat']
    long = request.form['long']
    source = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={long}"
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

    return ('<h3> Your summarized forecast is: </h3> %s <br/> <a href="/">Back Home</a>'
    % (weather.to_html(header="true", table_id="table")))

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    return result

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3021, debug = True)
import requests
import pandas as pd
from bs4 import BeautifulSoup

# examples from:
# https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/

page = requests.get("https://dataquestio.github.io/web-scraping-pages/simple.html")
page.status_code
print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

list(soup.children)
[type(item) for item in list(soup.children)]
html = list(soup.children)[2]
list(html.children)
body = list(html.children)[3]
list(body.children)
p = list(body.children)[1]
p.get_text()


soup = BeautifulSoup(page.content, 'html.parser')
soup.find_all('p')[0].get_text()

page = requests.get("https://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')
soup.find_all('p', class_='outer-text')
soup.find_all(class_="outer-text")

soup.find_all(id="first")
soup.select("div p")

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")

forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())

period = tonight.find(class_ = "period-name").get_text()
short_desc = tonight.find(class_ = "short-desc").get_text()
temp = tonight.find(class_ = "temp").get_text()
img = tonight.find("img")
desc = img['title']

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})

temp_nums = weather["temp"].str.extract("(?P<a>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')

weather["temp_num"].mean()

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night

weather[is_night]


page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
periods = [pt.get_text() for pt in seven_day.select(".tombstone-container .period-name")]
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})
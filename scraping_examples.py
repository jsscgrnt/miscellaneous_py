import requests
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
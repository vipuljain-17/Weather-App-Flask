import requests
from bs4 import BeautifulSoup

city_name = "pryaagraj"
query = 'search?q='
weather_statement = '+weather'
url = 'https://bing.com/' + query + city_name + weather_statement
page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
soup = BeautifulSoup(page.content, 'html.parser')

temp = soup.find("div",{"class": "wtr_currTemp b_focusTextLarge"}).text
print(f"Temperature currently: {temp}" + u"\u2103")

current_conditions = soup.find("div", {"class": "wtr_caption"})
print("Current Conditions: " + current_conditions.text)

precipitation = soup.find("div", {"class": "wtr_currPerci"})
print(precipitation.text)

wind_speed = soup.find("div", {"class": "wtr_currWind"})
print(wind_speed.text)
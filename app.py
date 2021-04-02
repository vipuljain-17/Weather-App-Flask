from flask import Flask, render_template, request
import pandas as pd
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

cities_names =  pd.read_csv("indian_cities.csv")
def search_city(city_name):
    if city_name.lower() in cities_names['City'].values:
        return cities_names[cities_names['City'] == city_name.lower()].values[0][2]
    else:
        return False

def query_temp(city_name, state_name, val):
    city_name = city_name.lower()
    url = 'https://bing.com/search?q=' + city_name + '+weather'
    page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})
    soup = BeautifulSoup(page.content, 'html.parser')

    temp = soup.find("div",{"class": "wtr_currTemp b_focusTextLarge"}).text
    #print(f"Temperature currently: {temp}" + u"\u2103")

    current_conditions = soup.find("div", {"class": "wtr_caption"})
    #print("Current Conditions: " + current_conditions.text)

    precipitation = soup.find("div", {"class": "wtr_currPerci"})
    #print(precipitation.text)

    wind_speed = soup.find("div", {"class": "wtr_currWind"})
    #print(wind_speed.text)

    result = {
            "region": city_name.capitalize(),
            "state": state_name.capitalize(),
            "temp_now": temp,
            "weather_now": current_conditions.text,
            "precipitation": precipitation.text,
            "wind": wind_speed.text,
            "check": val
        }
    
    return result

@app.route("/", methods = ["GET","POST"])
def home_view():
    result = None
    if request.method == "POST":
        val = 1
        city_name = request.form['city']
        if city_name == "":
            city_name = "Delhi"
            val = 0

        state_name = search_city(city_name)
        if state_name == False:
            city_name = "Delhi"
            state_name = "Delhi"
            val = 0

        result = query_temp(city_name, state_name, val)
                
    return render_template("home.html", result = result)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Page Not Found. Check your URL</h1>"

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
from flask.globals import request
import requests
from _datetime import datetime


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/weatherapp', methods=['POST', 'GET'])
def weatherapp():
    city = request.form['city']
    url = "https://community-open-weather-map.p.rapidapi.com/find"

    querystring = {"q": f"{city}"}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "your authentication key here"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)



    if not response.json()['list']:
        return "<h1>City not found</h1>"

    else:
        rain = response.json()['list'][0]['weather'][0]['description']

        speed = response.json()['list'][0]['wind']['speed']

        temp = response.json()['list'][0]['main']['temp']
        temperature = round(temp - 273.15)

        unix_date = response.json()['list'][0]['dt']
        date = datetime.fromtimestamp(unix_date)
        formatted_date = date.strftime('%d-%m-%y')

        return render_template('weather.html', date=formatted_date, temperature=temperature, wind_speed=speed,
                               city=city.upper(), rain=rain)


if __name__ == '__main__':
    app.run()

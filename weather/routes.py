from flask import render_template, request, flash, redirect, url_for
from weather import app, db
from weather.models import City
import requests


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    city = 'Yangon'
    if request.method == 'POST':
        city = request.form.get('city')

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=06bb9073587b0c1190b6b110119e6d93'
    req = requests.get(url.format(city)).json()

    print(req)

    weather_data = {
        'city': city,
        'temperature': req['main']['temp'],
        'desc': req['weather'][0]['description'],
        'img': req['weather'][0]['icon']
    }
    print(weather_data)

    return render_template("index.html", weather=weather_data)


@app.route("/add/<string:name>", methods=['POST'])
def add(name):
    if request.method == 'POST':
        c1 = City(name=name)
        db.session.add(c1)
        db.session.commit()
        flash(f'Added to List!', 'success')
    return redirect(url_for('home'))

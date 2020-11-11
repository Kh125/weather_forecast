from flask import render_template, request, flash, redirect, url_for,session
from weather import app, db
from weather.models import City
import requests


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'city' in session:
      city = session['city']
    else:
      city = 'Yangon'
    if request.method == 'POST':
     city = request.form.get('city')
     session['city'] = city
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=06bb9073587b0c1190b6b110119e6d93'
    req = requests.get(url.format(city)).json()
    if req['cod'] != 200:
      weather_data = {
        'city': city,
        'cod':req['cod'],
        'message':req['message']
      }
    else:
      weather_data = {
        'cod':req['cod'],
        'city': city,
        'std_city':req['name'],
        'temperature': req['main']['temp'],
        'desc': req['weather'][0]['description'],
        'img': req['weather'][0]['icon'],
        'humidity': req['main']['humidity'],
        'feels':req['main']['feels_like'],
        'speed':req['wind']['speed'],
        'deg':req['wind']['deg']
      }
    count = 1
    if 'county' not in session:
      count = 0
    count += 1
    session['county'] = count
    return render_template("index.html", weather=weather_data)

@app.route("/list",methods=['POST','GET'])
def show_all():
  city1 = City.query.all()
  city_data = []
  url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=06bb9073587b0c1190b6b110119e6d93'
  for ct in city1:
    req_all = requests.get(url.format(ct.name)).json()
    if req_all['cod'] != 200:
      weather_data = {
        'city': req_all['name'],
        'cod':req_all['cod'],
        'message':req_all['message']
      }
    else:
      weather_data = {
        'cod':req_all['cod'],
        'city': ct.name,
        'std_city':req_all['name'],
        'temperature': req_all['main']['temp'],
        'desc': req_all['weather'][0]['description'],
        'img': req_all['weather'][0]['icon'],
        'humidity': req_all['main']['humidity'],
        'feels':req_all['main']['feels_like'],
        'speed':req_all['wind']['speed'],
        'deg':req_all['wind']['deg']
      }

      city_data.append(weather_data)
  
  return render_template('custom.html',city = city_data)

@app.route("/add/<string:name>", methods=['POST'])
def add(name):
    if request.method == 'POST':
      c1 = City.query.filter_by(name=name).first()
      if c1:
        flash(f'Already in the List!', 'info')
        return redirect(url_for('home'))      
      else:
        c1 = City(name=name)
        db.session.add(c1)
        db.session.commit()
        flash(f'Added to List!', 'success')
    return redirect(url_for('home'))


@app.route("/remove/<string:name>", methods=['POST'])
def remove(name):
    if request.method == 'POST':
      c1 = City.query.filter_by(name=name).first()
      if c1:
        db.session.delete(c1)
        db.session.commit()
        flash(f'Remove from the List!', 'info')
        return redirect(url_for('show_all'))
      else:      
        flash(f'This city doesn\'t exist in List!', 'success')
    return redirect(url_for('show_all'))



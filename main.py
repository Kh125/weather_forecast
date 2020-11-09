from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

class City(db.Model):
  ID = db.Column(db.Integer,primary_key = True)
  NAME = db.Column(db.String(60),nullable=False)


@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
  city = 'Yangon'
  if request.method == 'POST':
    city = request.form.get('city')

  url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=06bb9073587b0c1190b6b110119e6d93' 
  req = requests.get(url.format(city)).json()

  weather_data = {
    'city':city,
    'temperature': req['main']['temp'],
    'desc':req['weather'][0]['description'],
    'img':req['weather'][0]['icon']
  }
  print(weather_data)

  return render_template("index.html",weather=weather_data)


app.run(host="0.0.0.0",port="8080")
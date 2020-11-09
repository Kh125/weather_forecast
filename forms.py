from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class GetWeather(FlaskForm):
  cityname = StringField('City Name',validators=[DataRequired()])
  
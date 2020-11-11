from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired,ValidationError
from weather.models import City


class GetWeather(FlaskForm):
  cityname = StringField('City Name',validators=[DataRequired()])
  
  def validate_cityname(self,cityname):
    c1 = City.query.filter_by(name=cityname).first()
    if c1:
      raise ValidationError('Already added to list')
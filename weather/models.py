from weather import db

class City(db.Model):
  ID = db.Column(db.Integer,primary_key = True)
  NAME = db.Column(db.String(60),nullable=False)

from weather import db

class City(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  name = db.Column(db.String(60),nullable=False,unique=True)
  def __repr__(self):
    return f"City('{self.id}','{self.name}')"
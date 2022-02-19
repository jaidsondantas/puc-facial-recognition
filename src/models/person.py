from sql_alchemy import banco

class PersonModel(banco.Model):
  __tablename__ = 'people'

  id = banco.Column(banco.String, primary_key= True)
  name = banco.Column(banco.String(3000))

  def __init__(self, id, name):
    self.id = id
    self.name = name


  def json(self):
    return {
      'id': self.id,
      'name': self.name
    }
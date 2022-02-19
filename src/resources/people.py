from flask_restful import Resource

class People(Resource):
  def get(self):
    return {'data': True}




